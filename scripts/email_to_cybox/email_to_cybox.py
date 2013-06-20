#!\usr\bin\env python

"""
Converts raw email to CybOX representation

Email to CybOX v2.0 Translator
2013 - Bryan Worrell & Greg Back - The MITRE Corporation

Requires python-cybox
"""

# Script version
__version__ = '2.0.0b1'

# Standard Library imports
import argparse
import base64
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

#Third Party imports

#pip install dnspython
import dns.resolver
#pip install python-whois
import whois
import whois.parser

# CybOX imports
from cybox import ObjectReference
from cybox.common import DateTime, Hash, HexBinary, PositiveInteger, String
from cybox.core import Observables
from cybox.objects.address_object import Address, EmailAddress
from cybox.objects.dns_query_object import (DNSQuery, DNSQuestion,
        DNSResourceRecords)
from cybox.objects.dns_record_object import DNSRecord
from cybox.objects.email_message_object import (Attachments, EmailHeader,
        EmailMessage, EmailRecipients, LinkReference, Links)
from cybox.objects.file_object import File
from cybox.objects.uri_object import URI
from cybox.objects.whois_object import (WhoisContact, WhoisContacts,
        WhoisEntry, WhoisNameservers, WhoisRegistrar, WhoisStatus,
        WhoisStatuses)


__all__ = ["EmailParser"]

# Global Variables
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

# Regular Expressions used when parsing
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
        url = HTTP_WHOIS_URL + domain

        request = urllib2.Request(url)
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
            print 'Cannot reach the WHOIS http service because:' + str(e.reason)
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
        record = {}

        #TODO: process entire lists if they exist
        if response.registrar:
            record['registrar'] = response.registrar[0]
        if response.whois_server:
            record['whois_server'] = response.whois_server[0]
        if response.domain_name:
            record['domain_name'] = response.domain_name[0]
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
            return EmailAddress(match.group(1))
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

        return headers

    def __create_url_object(self, url):
        """ Creates a CybOX URIObjectType object """
        if not url:
            return None

        if self.__verbose_output:
            print "** creating uri object for: " + url

        return URI(url, URI.TYPE_URL)

    def __create_domain_name_object(self, domain):
        """ Creates a CybOX URIObjectType object """
        if not domain:
            return None

        if self.__verbose_output:
            print "** creating domain name object for: " + str(domain)

        return URI(domain, URI.TYPE_DOMAIN)

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

        whois = WhoisEntry()

        record['status'] = ['OK' if status == 'ACTIVE' else status for status in record['status']]

        #Only build registrar info objects if we have the relevant info
        if (record['registrar'] or record['whois_server'] or
                    record['registrar_address'] or record['referral_url'] or
                    record['registrar_contacts']):
            registrar = WhoisRegistrar()
            registrar.name = String(record.get('registrar'))
            registrar.address = String(record.get('registrar_address'))
            registrar.whois_server = URI(record.get('whois_server'))
            registrar.referral_url = URI(record.get('referral_url'))

            contacts = WhoisContacts()
            for email in record['registrar_contacts']:
                contact = WhoisContact()
                contact.contact_type = 'ADMIN'
                contact.name = String(record.get('registrar'))
                contact.email_address = EmailAddress(email)

                contacts.append(contact)
            registrar.contacts = contacts

            whois.registrar_info = registrar

        whois.domain_name = self.__create_domain_name_object(record.get('domain_name'))

        nservers = WhoisNameservers()
        for url in record.get('name_servers', []):
            nservers.append(self.__create_url_object(url))
        if nservers:
            whois.nameservers = nservers

        status = WhoisStatuses()
        for s in record.get('status', []):
            status.append(WhoisStatus(s))
        if status:
            whois.status = status

        whois.updated_date = DateTime(record.get('updated_date'))
        whois.creation_date = DateTime(record.get('creation_date'))
        whois.expiration_date = DateTime(record.get('expiration_date'))

        return whois

    def __create_dns_query_object(self, domain, record_type, nameserver=None):
        """Creates a CybOX DNSQueryType Object"""
        question = DNSQuestion()
        question.qname = self.__create_domain_name_object(domain)
        question.qtype = String(record_type)
        question.qclass = String('IN')

        query = DNSQuery()
        query.successful = False
        query.question = question

        return query

    def __create_dns_record_object(self, domain, record_type, nameserver=None):
        """Creates a CybOX DNSRecordType Object"""
        record = self.__get_dns_record(domain, record_type, nameserver)
        if not record:
            return None

        dns_record = DNSRecord()
        dns_record.domain_name = self.__create_domain_name_object(record.get('Domain_Name'))
        dns_record.ip_address = self.__create_ip_address_object(record.get('IP_Address'))
        dns_record.entry_type = String(record.get('Entry_Type'))
        dns_record.flags = HexBinary(record.get('Flags'))
        dns_record.record_data = record.get('Record_Data')

        return dns_record

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
            print "** creating ip address object for: " + str(ip_addr)

        if ':' in str(ip_addr):
            category = Address.CAT_IPV6
        else:
            category = Address.CAT_IPV4

        return Address(ip_addr, category)

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

    def __parse_urls(self, body):
        """Parses out URLs from the body. Returns a tuple of lists of URI 
        and Domain objects, respectively."""
        unique_urls = set()
        unique_domains = set()

        if self.__verbose_output:
            print "** parsing urls from email body"

        for match in URL_PATTERN.findall(body):
            url = match[0]
            unique_urls.add(url)
            domain = whois.extract_domain(url)
            unique_domains.add(domain)

        # Mapping of domain names to the objects that reference them
        domain_map = {}

        # List of Domain and related (DNS, Whois) objects to be returned
        domain_list = []

        # List of URI objects to be returned
        url_list = []

        for domain in unique_domains:
            domain_objs = self.__create_domain_objs(domain)
            # Save all the related objects in the correct order in the list.
            domain_list.extend(self.__reorder_domain_objs(domain_objs))
            # Save this domain object for linking to URLs
            domain_map[domain] = domain_objs['URI']

        for u in unique_urls:
            if self.include_url_objects:
                url = self.__create_url_object(u)

            # Retrieve the Domain from the dictionary
            domain = domain_map[whois.extract_domain(u)]
            # Add relationships between the URL and the domain
            domain.add_related(url, 'Extracted_From', inline=False)
            domain.add_related(url, 'FQDN_Of', inline=False)
            url.add_related(domain, 'Contains', inline=False)

            url_list.append(url)

        return (url_list, domain_list)

    def __create_dns_objs(self, query, uri, dns_record):
        """given a dns query, the uri of the domain, a dns record for the domain, and an address class,
        adds the necessary relationships and returns a container for the resolved address and the record """
        address = dns_record.ip_address

        resource_records = DNSResourceRecords()
        resource_records.append(dns_record)
        query.answer_resource_records = resource_records
        query.successful = True

        dns_record.add_related(uri, 'Characterizes', inline=False)
        dns_record.add_related(query, 'Contained_Within', inline=False)
        query.add_related(dns_record, 'Contains', inline=False)
        uri.add_related(dns_record, 'Characterized_By', inline=False)
        uri.add_related(address, 'Resolved_To', inline=False)
        address.add_related(uri, 'Resolved_To', inline=False)
        address.add_related(query, 'Contained_Within', inline=False)
        address.add_related(dns_record, 'Contained_Within', inline=False)

    def __create_domain_objs(self, domain):
        """Creates new object containers for new domains and objects related to domains (whois, dns, addresses)"""

        new_objs = {'URI': None,
                    'Whois': None,
                    'DNSQueryV4': None,
                    'DNSResultV4': None,
                    'ipv4': None,
                    'DNSQueryV6': None,
                    'DNSResultV6': None,
                    'ipv6': None}

        if self.include_domain_objects:
            domain_obj = self.__create_domain_name_object(domain)

        if self.whois or self.http_whois:
            whois_obj = self.__create_whois_object(domain)

            if whois_obj:
                new_objs['Whois'] = whois_obj
                if domain_obj:
                    whois_obj.add_related(domain_obj, 'Characterizes', inline=False)
                    domain_obj.add_related(whois_obj, 'Characterized_By', inline=False)

        #get ipv4 dns record for domain
        if self.dns:
            query_obj = self.__create_dns_query_object(domain, 'A')
            if domain_obj:
                query_obj.add_related(domain_obj, 'Searched_For', inline=False)
                domain_obj.add_related(query_obj, 'Searched_For_By', inline=False)

            new_objs['DNSQueryV4'] = query_obj
            dns_record_obj = self.__create_dns_record_object(domain, 'A', NAMESERVER)
            if dns_record_obj:
                new_objs['DNSResultV4'] = self.__create_dns_objs(query_obj, domain_obj, dns_record_obj)
                new_objs['ipv4'] = dns_record_obj.ip_address

            #get ipv6 dns record for domain
            query6_obj = self.__create_dns_query_object(domain, 'AAAAA')
            if domain_obj:
                query6_obj.add_related(domain_obj, 'Searched_For', inline=False)
                domain_obj.add_related(query6_obj, 'Searched_For_By', inline=False)

            new_objs['DNSQueryV6'] = query6_obj
            dns_record6_obj = self.__create_dns_record_object(domain, 'AAAA', NAMESERVER)
            if dns_record6_obj:
                new_objs['DNSResultV6'] = self.__create_dns_objs(query6_obj, domain_obj, dns_record6_obj)
                new_objs['ipv6'] = dns_record6_obj.ip_address

        new_objs['URI'] = domain_obj
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
                f.add_related(message, "Contained_In", inline=False)

        if self.include_raw_headers:
            raw_headers_str = self.__get_raw_headers(msg)
            message.raw_header = String("<![CDATA[ " + raw_headers_str + " ]]>")

        # need this for parsing urls AND raw body text
        raw_body = "\n".join(self.__get_raw_body_text(msg)).strip()

        if self.include_raw_body:
            message.raw_body = String("<![CDATA[ " + raw_body + " ]]>")

        if self.include_urls:
            (url_list, domain_list) = self.__parse_urls(raw_body)
            if url_list:
                links = Links()
                for u in url_list:
                    links.append(LinkReference(u.parent.id_))
                message.links = links

        # Return a list of all objects we've built
        return [message] + files + url_list + domain_list

    def generate_cybox_from_email_file(self, data):
        """ Returns a CybOX Email Message Object """
        msg = self.__parse_email_file(data)
        return Observables(self.__parse_email_message(msg))

    def generate_cybox_from_email_str(self, data):
        """ Returns a CybOX Email Message Object """
        msg = self.__parse_email_string(data)
        return Observables(self.__parse_email_message(msg))

    def write_cybox(self, cybox_obj, filename):
        """Write the CyBOX Email Message Object to file """
        if self.__verbose_output:
            print "** writing email message object to file: " + filename

        with open(filename, 'w') as outfile:
            cybox_obj.to_obj().export(outfile, 0)
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
