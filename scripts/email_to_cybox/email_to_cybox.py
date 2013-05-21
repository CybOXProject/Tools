#!\usr\bin\env python

"""
Converts raw email to CybOX representation

Email to CybOX v1.0 Translator
v0.2 BETA // Compatible with CybOX v1.0
2012 - Bryan Worrell - The MITRE Corporation
"""

import argparse
import base64
from collections import defaultdict
import datetime
import email
import hashlib
import os
import quopri
import re
import socket
import sys
import time
import traceback
import urllib2
import uuid


#cybox bindings
#import cybox.bindings.cybox_common_types_1_0 as common
#import cybox.bindings.cybox_core_1_0 as cybox
#import cybox.bindings.email_message_object_1_2 as email_message_object
#import cybox.bindings.uri_object_1_2 as uri_object
#import cybox.bindings.file_object_1_3 as file_object
#import cybox.bindings.address_object_1_2 as address_object
#import cybox.bindings.whois_object_1_0 as whois_object
#import cybox.bindings.dns_query_object_1_0 as dns_query_object
#import cybox.bindings.dns_record_object_1_1 as dns_record_object

#pip install dnspython
import dns.resolver
#pip install python-whois
import whois
import whois.parser

import cybox.core
from cybox.common import DateTime, Hash, PositiveInteger, String
from cybox.objects.address_object import Address
from cybox.objects.email_message_object import (Attachments, EmailHeader,
        EmailMessage, EmailRecipients)
from cybox.objects.file_object import File


__all__ = ["EmailParser"]

# BEGIN GLOBAL VARIABLES
VERBOSE_OUTPUT = False

#TODO: Add Received Header support
ALLOWED_HEADER_FIELDS = ('to', 'cc', 'bcc', 'from', 'subject',
                         'in-reply-to', 'date', 'message-id', 'sender',
                         'reply-to', 'errors-to', 'boundary', 'content-type',
                         'mime-version', 'precedence', 'user-agent',
                         'x-mailer', 'x-originating-ip', 'x-priority')

HTTP_WHOIS_URL = 'http://whoiz.herokuapp.com/lookup.json?url='
NAMESERVER = None
# END GLOBAL VARIABLES

EMAIL_PATTERN = re.compile('([\w\-\.+]+@(\w[\w\-]+\.)+[\w\-]+)')

# Regex taken from Daring Fireball and modified:
#   http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# The original is considered under public domain.

URL_RE = r"""(?i)\b((?:(https?|ftp)://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))"""
URL_PATTERN = re.compile(URL_RE, re.VERBOSE | re.MULTILINE)


class EmailParser:
    """Translates raw email into a CybOX Email Message Object"""

    __verbose_output = False
    __email_obj_container = None

    def __init__(self, verbose=False):
        self.__verbose_output = verbose
        self.__email_obj_container = self._newObjContainer(self.__create_cybox_id("object"), None)

        self.inline_files = False

        self.include_urls = True
        self.include_attachments = True
        self.include_raw_body = True
        self.include_raw_headers = True
        self.include_url_objects = True
        self.include_domain_objects = True

        self.dns = False
        self.whois = False
        self.http_whois = False

        # By default, include all headers. This can be modified by the caller.
        self.headers = ALLOWED_HEADER_FIELDS

    class _newObjContainer:
        """Private class for storing new objects and their relationships"""
        def __init__(self, idref, obj):
            self.idref = idref
            self.obj = obj
            self.relationships = []

        def add_relationship(self, idref, type_, relationship):
            self.relationships.append({'idref': idref, 'type': type_, 'relationship': relationship})

        def get_relationship_objects(self):
            related_objects = cybox.RelatedObjectsType()
            for r in self.relationships:
                related_object = cybox.RelatedObjectType(idref=r['idref'], type_=r['type'], relationship=r['relationship'])
                related_objects.add_Related_Object(related_object)
            return related_objects

    def __get_email_obj_id(self):
        return self.__email_obj_container.idref

    def __get_email_obj_container(self):
        return self.__email_obj_container

    def __add_email_obj_relationship(self, idref, type_, relationship):
        self.__email_obj_container.add_relationship(idref, type_, relationship)

    def __parse_email_string(self, data):
        """ Returns an email.Message object """
        if self.__verbose_output:
            print "** parsing email input string"

        msg = email.message_from_string(data)
        return msg

    def __parse_email_file(self, data):
        """ Returns an email.Message object

        @data can be sys.stdin or a file-like object """
        if self.__verbose_output:
            print "** parsing email input file"

        msg = email.message_from_file(data)
        return msg

    def __create_cybox_id(self, item_type="guid"):
        """ Returns a unique cybox id """
        return "cybox:" + item_type + "-" + str(uuid.uuid1())

    def __get_email_id(self, item_type="guid"):
        """ Returns a unique cybox id for the Email message Object"""
        if self._EMAIL_OBJECT_ID:
            return EMAIL_OBJECT_ID
        else:
            EMAIL_OBJECT_ID = self.__create_cybox_id()
            return EMAIL_OBJECT_ID

    def __get_attachment_created_date(self, msg):
        """ Returns the creation date of the attachment if provided
        by the content-disposition header """
        content_disposition = msg.get('content-disposition').lower()
        create_pattern = re.compile('creation-date="([\w\s\:\-\+\,]+)"')
        match = create_pattern.search(content_disposition)

        xml_created_date = None
        if match:
            create_date = match.group(1)
            create_date_tup = email.utils.parsedate_tz(create_date)
            xml_created_date = self.__get_xml_datetime_fmt(create_date_tup)

        return xml_created_date

    def __get_attachment_modified_date(self, msg):
        """ Returns the modified date of the attachment if provided
        by the content-disposition header """
        content_disposition = msg.get('content-disposition')
        mod_pattern = re.compile('modification-date="([\w\s\:\-\+\,]+)"')
        match = mod_pattern.search(content_disposition)

        xml_mod_date = None
        if match:
            mod_date = match.group(1)
            mod_date_tup = email.utils.parsedate_tz(mod_date)
            xml_mod_date = self.__get_xml_datetime_fmt(mod_date_tup)

        return xml_mod_date

    def __get_whois_record_http(self, domain):
        global HTTP_WHOIS_URL

        request = urllib2.Request(HTTP_WHOIS_URL + domain)
        request.add_header('Accept', 'application/json')
        request.add_header('Content-type', 'application/x-www-form-urlencoded')
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print 'The WHOIS http service failed to fulfill the request because:'
            print 'Error code: ', e.code
            print 'No Whois information for domain: ' + domain + ' will be captured.\n'
            return None
        except urllib2.URLError, e:
            print 'Cannot reach the WHOIS http service because:' + e.reason
            print 'No Whois information for domain: ' + domain + ' will be captured.\n'
            return None
        else:
            response_text = response.read()
            response_lower = response_text.lower()

        if '"error"' in response_lower or 'not found' in response_lower or 'no match' in response_lower:
            return None

        formatted_response = response_text.replace('\\r', '').replace('\\n', '\n')
        record = whois.WhoisEntry.load(domain, formatted_response)
        return self.__convert_whois_record(record)

    def __get_whois_record(self, domain):
        try:
            record = whois.whois(domain)
        except Exception, e:
            print 'The whois lookup for the domain: ' + domain + ' failed for the following reason:\n\n'
            print e
            return None

        return self.__convert_whois_record(record)

    def __convert_whois_record(self, response):
        """take a whois response and convert it into a dict with better formatted info"""
        record = defaultdict(lambda: None, status=[], registrar_contacts=[], name_servers=[])

        if response.registrar:
            record['registrar'] = response.registrar[0]
        if response.whois_server:
            record['whois_server'] = response.whois_server[0]
        if response.domain_name:
            record['domain_name'] = response.domain_name
        if response.referral_url:
            record['referral_url'] = response.referral_url[0]
        #These list comprehensions get rid of empty strings that the parser sometimes adds to the lists
        if response.status:
            record['status'] = [x.replace(' ', '_') for x in response.status if len(x.strip())]
        if response.emails:
            record['registrar_contacts'] = [x for x in response.emails if len(x.strip())]
        if response.name_servers:
            record['name_servers'] = [x for x in response.name_servers if len(x.strip())]

        #these dates can be datetimes or arrays of datetimes, not sure why
        if response.creation_date:
            if response.creation_date is list:
                record['creation_date'] = self.__get_xml_date_fmt(whois.parser.cast_date(response.creation_date[0]))
            else:
                record['creation_date'] = self.__get_xml_date_fmt(response.creation_date.timetuple())

        if response.updated_date:
            if response.updated_date is list:
                record['updated_date'] = self.__get_xml_date_fmt(whois.parser.cast_date(response.updated_date[0]))
            else:
                record['updated_date'] = self.__get_xml_date_fmt(response.updated_date.timetuple())

        if response.expiration_date:
            if response.expiration_date is list:
                record['expiration_date'] = self.__get_xml_date_fmt(whois.parser.cast_date(response.expiration_date[0]))
            else:
                record['expiration_date'] = self.__get_xml_date_fmt(response.expiration_date.timetuple())

        return record

    def __get_dns_record(self, domain, record_type, nameserver=None):
        record = None
        resolver = dns.resolver.Resolver()
        if nameserver:
            resolver.nameservers = [nameserver]

        try:
            dns_response = resolver.query(domain, record_type)
            record = {'Entry_Type': record_type, 'Domain_Name': domain, 'IP_Address': dns_response[0]}
            record['Record_Data'] = dns_response.response.to_text()
            #The spec for hex values seems to be no leading 0x, all upper case
            record['Flags'] = hex(dns_response.response.flags).replace('0x', '').upper()
        except Exception, e:
            return None

        return record

    def __create_cybox_files(self, msg):
        """Returns a list of CybOX File objects from the message.

        Attachments can be identified within multipart messages by their
        Content-Disposition header.
        Ex: Content-Disposition: attachment; filename="foobar.jpg"
        """

        files = []

        if self.__verbose_output:
            print "** parsing attachments"

        # extract the email attachments into their own FileObjectType objects
        if msg.is_multipart():
            for part in msg.get_payload():
                if 'content-disposition' in part:
                    # if it's an attachment-type, pull out the filename
                    # and calculate the size in bytes

                    file_name = part.get_filename()
                    file_data = part.get_payload(decode=True)

                    f = File()
                    f.file_name = file_name
                    f.size = len(file_data)
                    f.file_extension = os.path.splitext(file_name)[1]

                    #TODO: add support for created and modified dates
                    #modified_date = self.__get_attachment_modified_date(part)
                    #created_date = self.__get_attachment_created_date(part)

                    if self.__verbose_output:
                        print "** creating file object for: %s, size: %d bytes" % (f.file_name, f.size)

                    md5_hash = hashlib.md5(file_data).hexdigest()
                    f.add_hash(md5_hash)

                    #TODO: create relationships between File and EmailMessage objects
                    #file_obj_container.add_relationship(self.__get_email_obj_id(), 'Email Message', 'Contained_Within')
                    #self.__add_email_obj_relationship(cybox_id, 'File', 'Contains')

                    files.append(f)

        return files

    def __get_xml_datetime_fmt(self, datetime_tup):
        """ Takes a tuple returned from email.util.parsedate_tz and converts it to an xs:dateTime formatted string with offset """
        year = datetime_tup[0]
        month = datetime_tup[1]
        day = datetime_tup[2]
        hours = datetime_tup[3]
        minutes = datetime_tup[4]
        seconds = datetime_tup[5]
        utc_offset = datetime_tup[-1]  # in seconds

        if utc_offset:
            # convert utc_offset to +/- 00:00 format
            if int(utc_offset) < 0:
                tzsign = -1
            else:
                tzsign = 1

            utc_offset_hours = int((tzsign * utc_offset) / 3600.0)
            utc_offset_minutes = ((tzsign * utc_offset) % 3600) / 60

        if utc_offset:
            if tzsign == -1:
                sign = "-"
            else:
                sign = "+"

            xml_datetime = "%02d-%02d-%02dT%02d:%02d:%02d%s%02d:%02d" % (year, month, day, hours, minutes, seconds, sign, utc_offset_hours, utc_offset_minutes)
        else:
            xml_datetime = "%02d-%02d-%02dT%02d:%02d:%02d" % (year, month, day, hours, minutes, seconds)

        return xml_datetime

    def __get_xml_date_fmt(self, datetime_tup):
        """ Takes a time tuple and converts it to an xs:date formatted string """
        year = datetime_tup[0]
        month = datetime_tup[1]
        day = datetime_tup[2]
        return "%02d-%02d-%02d" % (year, month, day)

    #TODO: make static method
    def _get_email_recipients(self, header):
        """Parse a string into an EmailRecipients list"""
        if not header:
            return None

        recips = EmailRecipients()
        for match in EMAIL_PATTERN.findall(header):
            recips.append(match[0])
        return recips

    #TODO: make static method
    def _get_single_email_address(self, header):
        """Extract a single email address from a header"""
        if not header:
            return None

        match = EMAIL_PATTERN.search(header)
        if match:
            return Address(match.group(1), Address.CAT_EMAIL)
        return None

    def __create_cybox_headers(self, msg):
        """ Returns a CybOX EmailHeaderType object """
        if self.__verbose_output:
            print "** parsing headers"

        headers = EmailHeader()

        #TODO: Add Received lines
        if 'to' in self.headers:
            headers.to = self._get_email_recipients(msg['to'])
        if 'cc' in self.headers:
            headers.cc = self._get_email_recipients(msg['cc'])
        if 'bcc' in self.headers:
            headers.bcc = self._get_email_recipients(msg['bcc'])
        if 'from' in self.headers:
            headers.from_ = self._get_single_email_address(msg['from'])
        if 'sender' in self.headers:
            headers.sender = self._get_single_email_address(msg['sender'])
        if 'reply-to' in self.headers:
            headers.reply_to = self._get_single_email_address(msg['reply-to'])
        if 'subject' in self.headers:
            headers.subject = String(msg['subject'])
        if 'in-reply-to' in self.headers:
            headers.in_reply_to = String(msg['in-reply-to'])
        if 'errors-to' in self.headers:
            headers.errors_to = String(msg['errors-to'])
        if 'date' in self.headers:
            headers.date = DateTime(msg['date'])
        if 'message-id' in self.headers:
            headers.message_id = String(msg['message-id'])
        if 'boundary' in self.headers:
            headers.boundary = String(msg['boundary'])
        if 'content-type' in self.headers:
            headers.content_type = String(msg['content-type'])
        if 'mime-version' in self.headers:
            headers.mime_version = String(msg['mime-version'])
        if 'precedence' in self.headers:
            headers.precedence = String(msg['precedence'])
        if 'user-agent' in self.headers:
            headers.user_agent = String(msg['user-agent'])
        if 'x-mailer' in self.headers:
            headers.x_mailer = String(msg['x-mailer'])
        if 'x-originating-ip' in self.headers:
            headers.x_originating_ip = Address(msg['x-originating-ip'],
                                               Address.CAT_IPV4)
        if 'x-priority' in self.headers:
            headers.x_priority = String(msg['x-priority'])

        return headers.to_obj()

    def __create_url_object(self, url):
        """ Creates a CybOX URIObjectType object """
        if not url:
            return None

        if self.__verbose_output:
            print "** creating uri object for: " + url
        uri_obj = uri_object.URIObjectType(type_="URL",
                                           Value=common.AnyURIObjectAttributeType(valueOf_=url))

        uri_obj.set_anyAttributes_({'xsi:type': 'URIObj:URIObjectType'})
        return uri_obj

    def __create_domain_name_object(self, domain):
        """ Creates a CybOX URIObjectType object """
        if not domain:
            return None

        if self.__verbose_output:
            print "** creating domain name object for: " + domain

        uri_obj = uri_object.URIObjectType(type_="Domain Name",
                                           Value=common.AnyURIObjectAttributeType(valueOf_=domain))

        uri_obj.set_anyAttributes_({'xsi:type': 'URIObj:URIObjectType'})

        return uri_obj

    def __create_whois_object(self, domain):
        """ Creates a CybOX WHOISObjectType object """
        if not domain:
            return None

        if(self.__verbose_output):
            print "** creating Whois object for: " + domain

        if self.http_whois:
            record = self.__get_whois_record_http(domain)
        else:
            record = self.__get_whois_record(domain)

        if not record:
            return None

        record['status'] = ['OK' if status == 'ACTIVE' else status for status in record['status']]

        #Only build registrar info objects if we have the relevant info
        registrar_info = None
        if record['registrar'] or record['whois_server'] or record['registrar_address'] or record['referral_url']:
            registrar_info = whois_object.RegistrarInfoType(Name=self.__create_string_object_attr_type(record['registrar']),
                                                            Address=self.__create_string_object_attr_type(record['registrar_address']),
                                                            Email_Address=None,
                                                            Phone_Number=None,
                                                            Whois_Server=self.__create_url_object(record['whois_server']),
                                                            Referral_URL=self.__create_url_object(record['referral_url']))

        registrar_contacts = []
        for email in record['registrar_contacts']:
            registrar_contacts.append(whois_object.RegistrarContactType(contact_type='ADMIN',
                                                                        Name=self.__create_string_object_attr_type(record['registrar']),
                                                                        Email_Address=self.__create_email_address_object(email),
                                                                        Phone_Number=None))

        whois_obj = whois_object.WhoisObjectType(Domain_Name=self.__create_domain_name_object(record['domain_name']),
                                                 Server_Name=None,
                                                 Nameserver=[self.__create_url_object(url) for url in record['name_servers']],
                                                 Status=[whois_object.WhoisStatusType(valueOf_=status) for status in record['status']],
                                                 Updated_Date=self.__create_date_object_attr_type(record['updated_date']),
                                                 Creation_Date=self.__create_date_object_attr_type(record['creation_date']),
                                                 Expiration_Date=self.__create_date_object_attr_type(record['expiration_date']),
                                                 Registrar_Info=registrar_info,
                                                 Registrar_Contact=registrar_contacts)

        whois_obj.set_anyAttributes_({'xsi:type': 'WhoisObj:WhoisObjectType'})
        return whois_obj

    def __create_dns_query_object(self, domain, record_type, nameserver=None):
        """Creates a CybOX DNSQueryType Object"""
        dns_question_obj = dns_query_object.DNSQuestionType(QName=self.__create_domain_name_object(domain),
                                                            QType=dns_query_object.DNSRecordType(valueOf_=record_type),
                                                            QClass=self.__create_string_object_attr_type('IN'))

        dns_query_obj = dns_query_object.DNSQueryObjectType(successful=False, Question=dns_question_obj)
        dns_query_obj.set_anyAttributes_({'xsi:type': 'DNSQueryObj:DNSQueryObjectType'})

        return dns_query_obj

    def __create_dns_record_object(self, domain, record_type, nameserver=None):
        """Creates a CybOX DNSRecordType Object"""
        record = self.__get_dns_record(domain, record_type, nameserver)
        if not record:
            return None

        dns_record_obj = dns_record_object.DNSRecordObjectType(Domain_Name=self.__create_domain_name_object(record['Domain_Name']),
                                                               IP_Address=self.__create_ip_address_object(record['IP_Address']),
                                                               Entry_Type=self.__create_string_object_attr_type(record['Entry_Type']),
                                                               Flags=self.__create_hex_binary_object_attr_type(record['Flags']),
                                                               Record_Data=record['Record_Data']
                                                              )
        dns_record_obj.set_anyAttributes_({'xsi:type': 'DNSRecordObj:DNSRecordObjectType'})
        return dns_record_obj

    def __create_email_address_object(self, email_addr):
        """ Returns a CybOX AddressType Object for use with Email addresses """
        if not email_addr:
            return None

        if self.__verbose_output:
            print "** creating email address object for: " + email_addr

        addr_obj = address_object.AddressObjectType(
                   category='e-mail',
                   Address_Value=self.__create_string_object_attr_type(email_addr))

        return addr_obj

    def __create_hash_object(self, md5_hash):
        """ Returns a CybOX HashType object for the given md5 hash """
        hash_name_type = common.HashNameType(valueOf_="MD5")
        hash_value_type = common.SimpleHashValueType(valueOf_=md5_hash)
        hash_type = common.HashType(Type=hash_name_type, Simple_Hash_Value=hash_value_type)

        return hash_type

    def __create_hash_list_object(self, list_hash_type_objects):
        """ Returns a CybOX HashListType object for the given list of HashType objects """
        hash_list_object = common.HashListType()
        for hash_type_object in list_hash_type_objects:
            hash_list_object.add_Hash(hash_type_object)
        return hash_list_object

    def __create_ip_address_object(self, ip_addr):
        """ Returns a CybOX AddressType Object for use with IPv4 or IPv6 addresses """
        if not ip_addr:
            return None

        if self.__verbose_output:
            print "** creating ip address object for: " + ip_addr

        if ':' in str(ip_addr):
            category = 'ipv6-addr'
        else:
            category = 'ipv4-addr'

        addr_obj = address_object.AddressObjectType(
                   Address_Value=self.__create_string_object_attr_type(ip_addr),
                   category=category)
        addr_obj.set_anyAttributes_({'xsi:type': 'AddressObj:AddressObjectType'})
        return addr_obj

    #TODO: delete
    def __create_string_object_attr_type(self, value):
        """ Returns a CybOX StringObjectAttributeType object with a value
        of @value """
        if not value:
            return None

        str_obj = common.StringObjectAttributeType(valueOf_=value)
        return str_obj

    def __create_date_time_object_attr_type(self, value):
        """ Returns a CybOX DateTimeObjectAttributeType object with a value
        of @value """
        if not value:
            return None
        datetime_obj = common.DateTimeObjectAttributeType(valueOf_=value)

        return datetime_obj

    def __create_date_object_attr_type(self, value):
        """ Returns a CybOX DateTimeObjectAttributeType object with a value
        of @value """
        if not value:
            return None

        date_obj = common.DateObjectAttributeType(valueOf_=value)

        return date_obj

    def __create_hex_binary_object_attr_type(self, value):
        """ Returns a CybOX HexBinaryObjectAttributeType object with a value
        of @value """
        if not value:
            return None

        hex_obj = common.HexBinaryObjectAttributeType(valueOf_=value)

        return hex_obj

    def __get_raw_body_text(self, msg):
        """ Extracts the body of the email message from the Message object.
        Multipart MIME documents can embed other multipart documents
        within them. As a result, a depth-first approach is taken to
        finding the body segments.

        Each textual MIME segment which is not an attachment or header
        is appended to a list of body parts."""
        raw_body = []

        #TODO: clean this up with message.walk
        if not msg.is_multipart():
            # text document attachments have a content type of text, so we have to filter them out
            if ('content-disposition' not in msg) and (msg.get_content_maintype() == 'text'):
                raw_body_str = msg.get_payload(decode=True)
                raw_body.append(raw_body_str)
        else:
            for part in msg.get_payload():
                raw_body.extend(self.__get_raw_body_text(part))

        return raw_body

    def __reorder_domain_objs(self, domain_obj_map):
        """ Given the results of __create_domain_objs, reorder them into a list so they are in the desired order in the final xml"""
        ordered_objs = [domain_obj_map['URI']]
        if domain_obj_map['Whois']:
            ordered_objs.append(domain_obj_map['Whois'])
        if domain_obj_map['DNSQueryV4']:
            ordered_objs.append(domain_obj_map['DNSQueryV4'])
        if domain_obj_map['DNSResultV4']:
            ordered_objs.append(domain_obj_map['DNSResultV4'])
        if domain_obj_map['ipv4']:
            ordered_objs.append(domain_obj_map['ipv4'])
        if domain_obj_map['DNSQueryV6']:
            ordered_objs.append(domain_obj_map['DNSQueryV6'])
        if domain_obj_map['DNSResultV6']:
            ordered_objs.append(domain_obj_map['DNSResultV6'])
        if domain_obj_map['ipv6']:
            ordered_objs.append(domain_obj_map['ipv6'])

        return ordered_objs

    def __parse_urls(self, list_body_tups):
        """ Parses out URLs from the list_body_tups input and returns a map of URIObjectType objects keyed by
        object id. Each URL in the map is unique. The input parameter, list_body_tups is a list of tuples: (encoding, body text).

        Regex taken from Daring Fireball: http://daringfireball.net/2010/07/improved_regex_for_matching_urls
        and modified. The original is considered under public domain"""
        map_urls = {}
        map_domains = {}
        list_observed_urls = []
        list_observed_domains = {}

        if(self.__verbose_output):
            print "** parsing urls from email body"

        url = r"""(?i)\b((?:(https?|ftp)://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))"""
        url_re = re.compile(url, re.VERBOSE | re.MULTILINE)

        for body_tup in list_body_tups:
            encoding = body_tup[0]
            body = body_tup[1]

            if encoding and encoding.lower() == "quoted-printable":
                body = quopri.decodestring(body)

            for match in url_re.findall(body):
                found_url = match[0]
                found_domain = whois.extract_domain(found_url)

                if found_url not in list_observed_urls:
                    list_observed_urls.append(found_url)
                    if self.include_url_objects:
                        url_id = self.__create_cybox_id()
                        url_obj_container = self._newObjContainer(url_id, self.__create_url_object(found_url))
                    else:
                        (url_id, url_obj_container) = (None, None)
                    if found_domain in list_observed_domains:
                        domain_obj = list_observed_domains[found_domain]
                    else:
                        domain_objs = self.__create_domain_objs(found_domain)
                        domain_obj = domain_objs['URI']
                        list_observed_domains[found_domain] = domain_obj
                        map_domains[found_domain] = self.__reorder_domain_objs(domain_objs)

                        # for obj_container in domain_related_objs.values():
                        #     if obj_container:
                        #         map_domains[found_domain][] = obj_container
                        #         map_domains[obj_container.idref] = obj_container

                    if domain_obj and url_id:
                        domain_obj.add_relationship(url_id, 'URL', 'Extracted_From')
                        domain_obj.add_relationship(url_id, 'URL', 'FQDN_Of')
                        url_obj_container.add_relationship(domain_obj.idref, 'URI', 'Contains')
                    if url_id:
                        url_obj_container.add_relationship(self.__get_email_obj_id(), 'Email Message', 'Contained_Within')
                        self.__add_email_obj_relationship(url_id, 'URL', 'Contains')
                        map_urls[found_url] = url_obj_container

        return (map_urls, map_domains)

    def __create_dns_objs(self, query_container, uri_container, dns_record_obj, address_class):
        """given a dns query, the uri of the domain, a dns record for the domain, and an address class,
        adds the necessary relationships and returns a container for the resolved address and the record """
        addr_container = self._newObjContainer(self.__create_cybox_id(), dns_record_obj.get_IP_Address())
        record_container = self._newObjContainer(self.__create_cybox_id(), dns_record_obj)

        #add dns record reference to dns query
        dns_record_ref = dns_record_object.DNSRecordObjectType(object_reference=record_container.idref)
        dns_record_ref.set_anyAttributes_({'xsi:type': 'DNSRecordObj:DNSRecordObjectType'})
        query_container.obj.set_Answer_Resource_Records(dns_query_object.DNSResourceRecordsType(Resource_Record=[dns_record_ref]))
        query_container.obj.set_successful(True)

        record_container.add_relationship(uri_container.idref, 'URI',  'Characterizes')
        record_container.add_relationship(query_container.idref, 'DNS Query',  'Contained_Within')
        query_container.add_relationship(record_container.idref, 'DNS Record',  'Contains')
        uri_container.add_relationship(record_container.idref, 'DNS Record', 'Characterized_By')
        uri_container.add_relationship(addr_container.idref, 'IP Address', 'Resolved_To')
        addr_container.add_relationship(uri_container.idref, 'URI', 'Resolved_To')
        addr_container.add_relationship(query_container.idref, 'DNS Query', 'Contained_Within')
        addr_container.add_relationship(record_container.idref, 'DNS Record', 'Contained_Within')

        return (addr_container, record_container)

    def __create_domain_objs(self, domain):
        """Creates new object containers for new domains and objects related to domains (whois, dns, addresses)"""
        global NAMESERVER

        new_objs = {'URI': None, 'Whois': None,
                    'DNSQueryV4': None, 'DNSResultV4': None, 'ipv4': None,
                    'DNSQueryV6': None, 'DNSResultV6': None, 'ipv6': None}

        if self.include_domain_objects:
            uri_container = self._newObjContainer(self.__create_cybox_id(), self.__create_domain_name_object(domain))
        else:
            uri_container = None

        if self.whois or self.http_whois:
            whois_obj = self.__create_whois_object(domain)
            if whois_obj:
                whois_container = self._newObjContainer(self.__create_cybox_id(), whois_obj)
                new_objs['Whois'] = whois_container
                if uri_container:
                    whois_container.add_relationship(uri_container.idref, 'URI', 'Characterizes')
                    uri_container.add_relationship(whois_container.idref, 'WHOIS', 'Characterized_By')

        #get ipv4 dns record for domain
        if self.dns:
            query_container = self._newObjContainer(self.__create_cybox_id(), self.__create_dns_query_object(domain, 'A'))
            if uri_container:
                query_container.add_relationship(uri_container.idref, 'URI', 'Searched_For')
                uri_container.add_relationship(query_container.idref, 'DNS Query', 'Searched_For_By')

            new_objs['DNSQueryV4'] = query_container
            dns_record_obj = self.__create_dns_record_object(domain, 'A', NAMESERVER)
            if dns_record_obj:
                (new_objs['ipv4'], new_objs['DNSResultV4']) = self.__create_dns_objs(query_container, uri_container, dns_record_obj, 'ipv4-addr')

            #get ipv6 dns record for domain
            query_container = self._newObjContainer(self.__create_cybox_id(), self.__create_dns_query_object(domain, 'AAAA'))
            if uri_container:
                query_container.add_relationship(uri_container.idref, 'URI', 'Searched_For')
                uri_container.add_relationship(query_container.idref, 'DNS Query', 'Searched_For_By')

            new_objs['DNSQueryV6'] = query_container
            dns_record_obj = self.__create_dns_record_object(domain, 'AAAA', NAMESERVER)
            if dns_record_obj:
                (new_objs['ipv6'], new_objs['DNSResultV6']) = self.__create_dns_objs(query_container, uri_container, dns_record_obj, 'ipv6-addr')

        new_objs['URI'] = uri_container
        return new_objs


    def __get_raw_headers(self, msg):
        """ Returns a string representation of the raw email headers found within the
        input Message msg"""
        raw_headers_str = ""

        for header_key_val in msg.items():
            raw_headers_str += "%s: %s\n" % (header_key_val[0], header_key_val[1])

        return raw_headers_str

    def __add_related_objects(self, obj, idref, type_, relationship="Contained Within"):
        """ Adds a RelatedObjectsType object to the input CybOX Object.
        In the context of an EmailMessageObjectType, each child object
        (objects representing attachments or urls) are related to the
        EmailMessageObject in that they are Contained_Within it.

        Later versions of CybOX will be amended to support the inverse
        relationship (An EmailMessageObject can point to its related
        child objects).
        """
        related_object = cybox.RelatedObjectType(idref=idref, type_=type_, relationship=relationship)
        related_objects = obj.get_Related_Objects()
        if not related_objects:
            related_objects = cybox.RelatedObjectsType()
            obj.set_Related_Objects(related_objects)

        related_objects.add_Related_Object(related_object)

    def __create_cybox_email_message_object(self, attachments=None, links=None, headers=None, email_server=None, raw_body=None, raw_headers=None):
        """ Creates/returns a CybOX EmailMessageType from the given input params

        + The Email_Server element is ambiguous and ignored. I'm not
          sure how to discover the server type/name without developing
          some home-brew signature method
        """

        email_message_obj = email_message_object.EmailMessageObjectType(
                                    Attachments=attachments,
                                    Links=links,
                                    Header=headers,
                                    Email_Server=email_server,
                                    Raw_Body=raw_body,
                                    Raw_Header=raw_headers)

        email_message_obj.set_anyAttributes_({'xsi:type': 'EmailMessageObj:EmailMessageObjectType'})

        return email_message_obj

    def __create_cybox_observable(self, obj_container):
        observable = cybox.ObservableType(id=self.__create_cybox_id("observable"))
        cybox_object = cybox.ObjectType(id=obj_container.idref)
        cybox_object.set_Defined_Object(obj_container.obj)
        cybox_object.set_Related_Objects(obj_container.get_relationship_objects())
        stateful_measure = cybox.StatefulMeasureType()
        stateful_measure.set_Object(cybox_object)
        observable.set_Stateful_Measure(stateful_measure)

        return observable

    def __create_cybox_observable_list(self, object_map):
        """ Generates a list of cybox observables given a map of object containers """
        list_observables = []
        for obj_id, obj_container in object_map.iteritems():
            list_observables.append(self.__create_cybox_observable(obj_container))

        return list_observables

    def __create_cybox_observables(self, map_objs):
        """ Generates a CybOX Observable Document from the input map of CybOX Objects."""
        # set up the email observable
        email_observable = cybox.ObservableType(id=self.__create_cybox_id("observable"))
        email_obj_map = map_objs['message']
        (email_id, email_obj) = email_obj_map.iteritems().next()
        email_stateful_measure = cybox.StatefulMeasureType()
        cybox_email_obj = cybox.ObjectType(id=email_id)
        cybox_email_obj.set_Defined_Object(email_obj)
        cybox_email_obj.set_Related_Objects(self.__get_email_obj_container().get_relationship_objects())
        email_stateful_measure.set_Object(cybox_email_obj)
        email_observable.set_Stateful_Measure(email_stateful_measure)
        list_observables = [email_observable]
        root_observables = cybox.ObservablesType(cybox_major_version="1", cybox_minor_version="0", Observable=list_observables)

        if self.include_attachments and not self.inline_files:
            list_observables.extend(self.__create_cybox_observable_list(map_objs['files']))

        #this song and dance is so we can get the objects in the final xml in a particular order
        #we append things to list_observables in the order we want
        if self.include_urls:
            for domain_name, domain_objs in map_objs['domains'].iteritems():
                #iterating over keys is necessary to modify the dict while looping over it
                for url_id in map_objs['urls'].keys():
                    url_obj = map_objs['urls'][url_id]
                    if domain_name == whois.extract_domain(url_obj.obj.Value.valueOf_):
                        list_observables.append(self.__create_cybox_observable(url_obj))
                        del map_objs['urls'][url_id]
                for obj in domain_objs:
                    list_observables.append(self.__create_cybox_observable(obj))

        return root_observables

    def __parse_email_message(self, msg):
        """ Parses the supplied message
        Returns a map of message parts expressed as cybox objects.

        Keys: 'message', 'files', 'urls'
        """

        message = EmailMessage()

        # Headers are required (for now)
        message.header = self.__create_cybox_headers(msg)


        if self.include_attachments:
            files = self.__create_cybox_files(msg)
            message.attachments = Attachments()
            for f in files:
                message.attachments.append(f.parent.id_)

        if self.include_raw_headers:
            raw_headers_str = self.__get_raw_headers(msg)
            message.raw_header = String("<![CDATA[ " + raw_headers_str + " ]]>")

        # need this for parsing urls AND raw body text
        raw_body = "\n".join(self.__get_raw_body_text(msg)).strip()
        print raw_body

        if self.include_raw_body:
            message.raw_body = String("<![CDATA[ " + raw_body + " ]]>")

        if self.include_urls:
            (map_urls, map_domains) = self.__parse_urls(raw_body)
            link_objs = [x.obj for x in map_urls.values()]
            cybox_links = email_message_object.LinksType(Link=link_objs)
        else:
            (map_urls, map_domains) = (None, None)
            cybox_links = None

        email_message_id = self.__get_email_obj_id()


        cybox_email_message_obj = self.__create_cybox_email_message_object(attachments=cybox_attachments,
                                                                           links=cybox_links,
                                                                           headers=cybox_headers,
                                                                           raw_body=cybox_raw_body,
                                                                           raw_headers=cybox_raw_headers)
        map_email_message = {email_message_id: cybox_email_message_obj}

        return {'message': map_email_message, 'files': files, 'urls': map_urls, 'domains': map_domains}

    def generate_cybox_from_email_file(self, data):
        """ Returns a CybOX Email Message Object """
        msg = self.__parse_email_file(data)
        map_objs = self.__parse_email_message(msg)
        observables = self.__create_cybox_observables(map_objs)
        return observables

    def generate_cybox_from_email_str(self, data):
        """ Returns a CybOX Email Message Object """
        msg = self.__parse_email_string(data)
        map_objs = self.__parse_email_message(msg)
        observables = self.__create_cybox_observables(map_objs)
        return observables

    def write_cybox(self, cybox_obj, filename):
        """Write the CyBOX Email Message Object to file """
        if self.__verbose_output:
            print "** writing email message object to file: " + filename

        cybox_obj.export(open(filename, 'w'), 0, name_='Observables',
        namespacedef_='xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
        xmlns:cybox="http://cybox.mitre.org/cybox_v1"\
        xmlns:AddressObj="http://cybox.mitre.org/objects#AddressObject"\
        xmlns:Common="http://cybox.mitre.org/Common_v1"\
        xmlns:FileObj="http://cybox.mitre.org/objects#FileObject"\
        xmlns:URIObj="http://cybox.mitre.org/objects#URIObject"\
        xmlns:EmailMessageObj="http://cybox.mitre.org/objects#EmailMessageObject"\
        xmlns:WhoisObj="http://cybox.mitre.org/objects#WhoisObject"\
        xmlns:DNSRecordObj="http://cybox.mitre.org/objects#DNSRecordObject"\
        xmlns:DNSQueryObj="http://cybox.mitre.org/objects#DNSQueryObject"\
        xsi:schemaLocation="http://cybox.mitre.org/Common_v1 http://cybox.mitre.org/XMLSchema/cybox_common_types_v1.0.xsd\
        http://cybox.mitre.org/objects#AddressObject http://cybox.mitre.org/XMLSchema/objects/Address/Address_Object_1.2.xsd\
        http://cybox.mitre.org/objects#FileObject http://cybox.mitre.org/XMLSchema/objects/File/File_Object_1.3.xsd\
        http://cybox.mitre.org/objects#URIObject http://cybox.mitre.org/XMLSchema/objects/URI/URI_Object_1.2.xsd\
        http://cybox.mitre.org/objects#EmailMessageObject http://cybox.mitre.org/XMLSchema/objects/Email_Message/Email_Message_Object_1.2.xsd\
        http://cybox.mitre.org/objects#WhoisObject http://cybox.mitre.org/XMLSchema/objects/Whois/Whois_Object_1.0.xsd\
        http://cybox.mitre.org/objects#DNSQueryObject http://cybox.mitre.org/XMLSchema/objects/DNS_Query/DNS_Query_Object_1.0.xsd\
        http://cybox.mitre.org/objects#DNSRecordObject http://cybox.mitre.org/XMLSchema/objects/DNS_Record/DNS_Record_Object_1.1.xsd\
        http://cybox.mitre.org/cybox_v1 http://cybox.mitre.org/XMLSchema/cybox_core_v1.0.xsd"')
# END CLASS


def main():
    global VERBOSE_OUTPUT
    global NAMESERVER

    description = "Converts raw email to CybOX representation"
    #TODO: make this look cleaner
    epilog = """
        Example: `cat email.txt | python email_to_cybox.py -o output.xml - ` \n
        Example: `python email_to_cybox.py -i foobar.txt -o output.xml` \n
        Example: `python email_to_cybox.pw -i foobar.txt -o output.xml --headers to,from,cc --exclude-urls` \n
        """

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-v', '--verbose', action='store_true',
            help="verbose output")

    parser.add_argument('-i', '--input', help="input file")
    parser.add_argument('-o', '--output', help="output file",
            default="output.xml")

    parser.add_argument('--inline-files', action='store_true',
            help="embed file object details in the attachment section")

    # TODO: convert these from negative to positive
    parser.add_argument('--exclude-attachments', action="store_true",
            help='exclude attachments from cybox email message object')
    parser.add_argument('--exclude-raw-body', action="store_true",
            help='exclude raw body from email message object')
    parser.add_argument('--exclude-raw-headers', action="store_true",
            help='exclude raw headers from email message object')
    parser.add_argument('--exclude-urls', action="store_true",
            help='do not attempt to parse urls from input')
    parser.add_argument('--exclude-domain-objs', action="store_true",
            help='do not create URI domain objects for found URLS')
    parser.add_argument('--exclude-url-objs', action="store_true",
            help='do not create URI objects for found URLs')

    parser.add_argument('--whois', action="store_true",
            help="attempt to perform s WHOIS lookup of domains found within "
                "the email and create a WHOIS record object")
    parser.add_argument('--http-whois', action="store_true",
            help="Use a HTTP WHOIS service that operates on port 80 (useful "
                "if port 43 is blocked by a firewall)")
    parser.add_argument('--dns', action="store_true",
            help="attempt to perform a dns lookup for domains within the "
                "email and create a DNS record object")

    parser.add_argument('--use-dns-server', metavar="DNS-SERVER",
            help=' use this DNS server for DNS lookup of domains')
    parser.add_argument('--headers',
            help="comma-separated list of header fields to be included in the "
                 "in the CybOX EmailMessage output. DO NOT INCLUDE SPACES. "
                 "Allowed fields: " + ", ".join(ALLOWED_HEADER_FIELDS) + ". "
                 "If not specified, all of these headers will be included if "
                 "present.")

    args = parser.parse_args()

    if args.input:
        #TODO: make sure this gets closed
        input_data = open(args.input, 'r')
    else:
        input_data = sys.stdin

    NAMESERVER = args.use_dns_server
    VERBOSE_OUTPUT = args.verbose

    translator = EmailParser(VERBOSE_OUTPUT)

    if args.headers:
        header_list = args.headers.split(',')
        for header in header_list:
            if header and (header not in ALLOWED_HEADER_FIELDS):
                parser.error("Unrecognized header field: %s" % header)
        translator.headers = header_list

    translator.inline_files = args.inline_files

    translator.include_raw_body = not args.exclude_raw_body
    translator.include_raw_headers = not args.exclude_raw_headers
    translator.include_attachments = not args.exclude_attachments
    translator.include_urls = not args.exclude_urls
    translator.include_url_objects = not args.exclude_url_objs
    translator.include_domain_objects = not args.exclude_domain_objs

    translator.dns = args.dns
    translator.whois = args.whois
    translator.http_whois = args.http_whois

    try:
        cybox_objects = translator.generate_cybox_from_email_file(input_data)
        translator.write_cybox(cybox_objects, args.output)
    except Exception, err:
        print('\n!! error: %s\n' % str(err))
        traceback.print_exc()

    if(VERBOSE_OUTPUT):
        print "** processing completed"


if __name__ == '__main__':
    main()
