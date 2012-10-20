""" 2012 - Bryan Worrell -The MITRE Corporation """

import hashlib
import base64
import uuid
import quopri
import sys
import traceback
import email
import re
import time
import datetime
import common_types_1_0 as common
import cybox_1_0 as cybox
import email_message_object_1_1 as email_message_object
import uri_object_1_1 as uri_object
import file_object_1_2 as file_object
import address_object_1_1 as address_object

# BEGIN GLOBAL VARIABLES

USAGE_TEXT = """
Email to CybOX v1.0 Translator
v0.2 BETA // Compatible with CybOX v1.0

Reads raw email text on stdin and converts the message to a cybox object

Usage: python email_to_cybox.py <flags>
Flags:
    -i <input_file>       : input from file
    -                     : input from stdin
    -o                    : <output file> (DEFAULT: 'output.xml')
    
    --inline-files        : embed file object details in the attachment section
    --exclude-opt-headers : exclude optional header fields from cybox email message object
    --exclude-attachments : exclude attachments from cybox email message object
    --exclude-raw-body    : exclude raw body from email message object 
    --exclude-raw-headers : exclude raw headers from email message object
    --exclude-urls        : do not attempt to parse urls from input
    --headers <one,two>   : comma separated list of header fields to be included
                            in the cybox email message object. SPACES NOT 
                            ALLOWED IN LIST OF FIELDS
                            fields('to', 'cc', 'bcc', 'from', 'subject', 'in-reply-to', 
                                   'date', 'message-id', 'sender', 'reply-to', 'errors-to')
    
    --opt-headers <one,two,...>      : comma separated list of optional header fields 
                                       to be included in the cybox email message object. 
                                       SPACES NOT ALLOWED IN LIST OF FIELDS.
                                       fields('boundary', 'content-type', 'mime-version',
                                      'precedence', 'x-mailer', 'x-originating-ip','x-priority')
    -h: Print help
    -v: Verbose error output
    
Example: `cat email.txt | python email_to_cybox.py -o output.xml - `
Example: `python email_to_cybox.py -i foobar.txt -o output.xml`
Example: `python email_to_cybox.pw -i foobar.txt -o output.xml --headers to,from,cc --exclude-urls`
"""

VERBOSE_OUTPUT = False

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

ALLOWED_HEADER_FIELDS = ('to', 'cc', 'bcc', 'from',
                         'subject', 'in-reply-to', 'date'
                         'message-id', 'sender', 'reply-to',
                         'errors-to')

ALLOWED_OPTIONAL_HEADER_FIELDS = ('boundary', 'content-type', 'mime-version',
                                  'precedence', 'x-mailer', 'x-originating-ip',
                                  'x-priority')

# END GLOBAL VARIABLES




# BEGIN CLASS

class email_translator:
    """Translates raw email into a CybOX Email Message Object"""

    (__OPT_INLINE_FILES, 
     __OPT_INC_URLS, 
     __OPT_INC_ATTACHMENTS, 
     __OPT_INC_RAW_BODY, 
     __OPT_INC_RAW_HEADERS, 
     __OPT_INC_HEADERS, 
     __OPT_INC_OPT_HEADERS ) = ('inline-files','include-urls', 'include-attachments', 
                                'include-raw-body', 'include-raw-headers', 'include-headers', 
                                'include-opt-headers')
    
    
    __map_general_options = {   'inline-files' : False,
                                'include-urls' : True,
                                'include-attachments' : True,
                                'include-raw-body' : True,
                                'include-raw-headers' : True,
                                'include-headers' : True,
                                'include-opt-headers' : True
                            }
    
    __map_header_options =  ('to','cc','bcc','from','subject', 'in-reply-to',
                             'date','message-id','sender', 'reply-to', 'errors-to')
    
    
    __map_optional_headers_options = ('boundary','content-type','mime-version',
                                      'precedence','x-mailer','x-originating-ip',
                                      'x-priority')

    __verbose_output = False
    
    
    
    """ Constructor """ 
    def __init__(self, verbose = False):
        self.__verbose_output = verbose

   
    def set_header_options(self, tuple_options):
        # The FROM field is required by the schema in v1.1
        tuple_options.append('from')
        self.__map_header_options = tuple_options
   
    def set_opt_header_options(self, tuple_options):
        self.__map_optional_headers_options = tuple_options
        
    def set_inline_files(self, enable):
        self.__map_general_options[self.__OPT_INLINE_FILES] = enable
        
    def set_include_urls(self, enable):
        self.__map_general_options[self.__OPT_INC_URLS] = enable
        
    def set_include_attachments(self, enable):
        self.__map_general_options[self.__OPT_INC_ATTACHMENTS] = enable
    
    def set_include_raw_body(self, enable):
        self.__map_general_options[self.__OPT_INC_RAW_BODY] = enable
           
    def set_include_raw_headers(self, enable):
        self.__map_general_options[self.__OPT_INC_RAW_HEADERS] = enable
        
    def set_include_headers(self, enable):
        self.__map_general_options[self.__OPT_INC_HEADERS] = enable
        
    def set_include_opt_headers(self, enable):
        self.__map_general_options[self.__OPT_INC_OPT_HEADERS] = enable
        
    def is_enabled_inline_files(self):
        return self.__map_general_options[self.__OPT_INLINE_FILES]
    
    def is_enabled_include_attachments(self):
        return self.__map_general_options[self.__OPT_INC_ATTACHMENTS]
        
    def is_enabled_include_urls(self):
        return self.__map_general_options[self.__OPT_INC_URLS]
    
    def is_enabled_include_raw_body(self):
        return self.__map_general_options[self.__OPT_INC_RAW_BODY]
    
    def is_enabled_include_raw_headers(self):
        return self.__map_general_options[self.__OPT_INC_RAW_HEADERS]
    
    def is_enabled_include_headers(self):
        return self.__map_general_options[self.__OPT_INC_HEADERS]
    
    def is_enabled_include_opt_headers(self):
        return self.__map_general_options[self.__OPT_INC_OPT_HEADERS]
    

    """ Returns an email.Message object """ 
    def __parse_email_string(self, data):
        if self.__verbose_output:
            print "** parsing email input string"
        
        msg = email.message_from_string(data)     
        return msg


    """ Returns an email.Message object 
        @data can be sys.stdin or a file-like object """ 
    def __parse_email_file(self, data):
        if self.__verbose_output:
            print "** parsing email input file"
        
        msg = email.message_from_file(data)     
        return msg



    """ Returns a unique cybox id """
    def __create_cybox_id(self, item_type = "guid"):
        return "cybox:" + item_type + "-" + str(uuid.uuid1())


    """ Returns file size of base64 decompressed attachment """

    def __get_file_size(self, base64_enc_data):
        num_bytes = len(base64.b64decode(base64_enc_data))
        return num_bytes


    """ Returns the MD5 hash for the given attachment.
        Because the attachments are base64 encoded,
        we need to decode the data and then run the 
        digest algorithm """
    def __get_attachment_md5(self, base64_enc_data):
        decoded = base64.b64decode(base64_enc_data)
        m = hashlib.md5()
        m.update(decoded)
        digest = m.hexdigest()
        return digest




    """ Returns the extension of the email attachment if it
        has one"""
    def __get_attachment_extension(self, msg):
        extension = None
        filename = msg.get_filename()
        dot_idx = filename.rfind('.')
    
        if(dot_idx != -1):
            extension = filename[dot_idx+1:]
        
        return extension



    """ Returns the creation date of the attachment if provided
        by the content-disposition header """
    def __get_attachment_created_date(self, msg):
        content_disposition = msg.get('content-disposition').lower()
        create_pattern = re.compile('creation-date="([\w\s\:\-\+\,]+)"')
        match = create_pattern.search(content_disposition)
        
        xml_created_date = None
        if( match ):
            create_date = match.group(1)
            create_date_tup = email.utils.parsedate_tz(create_date)
            xml_created_date = self.__get_xml_datetime_fmt(create_date_tup)
                      
        return xml_created_date


    """ Returns the modified date of the attachment if provided
        by the content-disposition header """
    def __get_attachment_modified_date(self, msg):
        content_disposition = msg.get('content-disposition')
        mod_pattern = re.compile('modification-date="([\w\s\:\-\+\,]+)"')
        match = mod_pattern.search(content_disposition)
        
        xml_mod_date = None
        if( match  ):
            mod_date = match.group(1)
            mod_date_tup = email.utils.parsedate_tz(mod_date)
            xml_mod_date = self.__get_xml_datetime_fmt(mod_date_tup)
                      
        return xml_mod_date
        

    """ Returns a map of file objects, keyed by a cybox uuid
        Attachments can be identified within multipart messages
        by their Content-Disposition header.
        Ex: Content-Disposition: attachment; filename="foobar.jpg"
    """
    def __create_cybox_files(self, msg):
        map_file_objs = {}
        
        if self.__verbose_output:
            print "** parsing attachments"
        
        # extract the email attachments into their own FileObjectType objects
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.has_key('content-disposition'):
                    # if it's an attachment-type, pull out the filename
                    # and calculate the size in bytes
                    filename = part.get_filename()
                    file_size = self.__get_file_size(part.get_payload())
                    md5_hash = self.__get_attachment_md5(part.get_payload())
                    size_in_bytes = common.UnsignedLongObjectAttributeType(
                                    valueOf_ = str(file_size))
                    modified_date = self.__get_attachment_modified_date(part)
                    created_date = self.__get_attachment_created_date(part)
                    extension = self.__get_attachment_extension(part)
                    
                    if(self.__verbose_output):
                        print "** creating file object for: " + filename + " size: " + str(file_size) + " bytes"

                    cybox_id = self.__create_cybox_id("object")
                    
                    hash_type_obj = self.__create_hash_object(md5_hash)
                    
                    file_obj = file_object.FileObjectType(
                               File_Name = self.__create_string_object_attr_type(filename),
                               File_Extension = self.__create_string_object_attr_type(extension),
                               Size_In_Bytes = size_in_bytes,
                               Hashes = self.__create_hash_list_object([hash_type_obj]),
                               Modified_Time = self.__create_string_object_attr_type(modified_date),
                               Created_Time = self.__create_date_time_object_attr_type(created_date))
                    
                    file_obj.set_anyAttributes_({'xsi:type' : 'FileObj:FileObjectType'})
                    map_file_objs[cybox_id] = file_obj
                #end if
            # end for
        # end if

        return map_file_objs
            
    
    """ Takes a tuple returned from email.util.parsedate_tz and converts it to an xs:dateTime formatted string with offset """
    def __get_xml_datetime_fmt(self, datetime_tup):
        year = datetime_tup[0]
        month = datetime_tup[1]
        day = datetime_tup[2]
        hours = datetime_tup[3]
        minutes = datetime_tup[4]
        seconds = datetime_tup[5]
        utc_offset = datetime_tup[-1] # in seconds
        
        if( utc_offset  ):
            # convert utc_offset to +/- 00:00 format
            if( int(utc_offset) < 0 ): tzsign = -1
            else: tzsign = 1
                
            utc_offset_hours =  int((tzsign * utc_offset) / 3600.0)
            utc_offset_minutes = ((tzsign * utc_offset) % 3600) / 60
        
        if( utc_offset ):
            if tzsign == -1 : sign = "-"
            else: sign = "+"
            
            xml_datetime = "%02d-%02d-%02dT%02d:%02d:%02d%s%02d:%02d" % (year, month, day, hours, minutes, seconds, sign, utc_offset_hours, utc_offset_minutes)
        else:
            xml_datetime = "%02d-%02d-%02dT%02d:%02d:%02d" % (year, month, day, hours, minutes, seconds)
            
        return xml_datetime
        
    

    """ Returns a CybOX EmailHeaderType object """ 
    def __create_cybox_headers(self, msg):
        email_pattern = re.compile('([\w\-\.+]+@(\w[\w\-]+\.)+[\w\-]+)')
           
        (TO, CC, BCC, FROM, SUBJECT, IN_REPLY_TO, DATE, MESSAGE_ID, SENDER, REPLY_TO, ERRORS_TO) = ('to', 'cc', 'bcc', 'from', 'subject', 'in_reply_to', 'date', 'message-id', 'sender', 'reply-to', 'errors-to')   
        
        if self.__verbose_output:
            print "** parsing headers"
                  
        msg_to = msg[TO] 
        msg_cc = msg[CC]
        msg_bcc = msg[BCC]
        msg_from = msg[FROM]
        msg_subject = msg[SUBJECT]
        msg_in_reply_to = msg[IN_REPLY_TO]
        msg_date = msg[DATE]
        msg_message_id = msg[MESSAGE_ID]
        msg_sender = msg[SENDER]
        msg_reply_to = msg[REPLY_TO]
        msg_errors_to = msg[ERRORS_TO]

        to_addrs = None
        if( msg_to and (TO in self.__map_header_options)  ): 
            to_addrs = email_message_object.EmailRecipientsType() 
            for match in email_pattern.findall(msg_to):
                email_addr_str = match[0] 
                addr_obj = self.__create_email_address_object(email_addr_str)
                to_addrs.add_Recipient(addr_obj)
            #end for
        #end if
            
        cc_addrs = None       
        if( msg_cc and (CC in self.__map_header_options)): 
            cc_addrs =  email_message_object.EmailRecipientsType() 
            for match in email_pattern.findall(msg_cc):
                email_addr_str = match[0]
                addr_obj = self.__create_email_address_object(email_addr_str)
                cc_addrs.add_Recipient(addr_obj)
            #end for
        #end if

        bcc_addrs = None
        if( msg_bcc and (BCC in self.__map_header_options)):
            bcc_addrs = email_message_object.EmailRecipientsType() 
            for match in email_pattern.findall(msg_bcc):
                email_addr_str = match[0]
                addr_obj = self.__create_email_address_object(email_addr_str)
                bcc_addrs.add_Recipient(addr_obj)
            #end for
        #end if

        from_addr = None 
        if( msg_from and (FROM in self.__map_header_options) ):
            from_addr_match = email_pattern.search(msg_from)
            if( from_addr_match ):
                from_addr_str = from_addr_match.group(1)
                from_addr = self.__create_email_address_object(from_addr_str)
            #end if
        else:
            # a From entry is required by the schema
            from_addr = self.__create_email_address_object("")
            
       
        sender_addr = None
        if( msg_sender and (SENDER in self.__map_header_options)  ):
            sender_addr_match = email_pattern.search(msg_sender)
            if( sender_addr_match  ):
                sender_addr_str = sender_addr_match.group(1)
                sender_addr = self.__create_email_address_object(sender_addr_str) 
            #end if
        #end if


        reply_to_addr = None
        if( msg_reply_to and (REPLY_TO in self.__map_header_options) ):
            reply_to_addr_match = email_pattern.search(msg_reply_to)
            if( reply_to_addr_match  ):
                reply_to_addr_str = reply_to_addr_match.group(1)
                reply_to_addr = self.__create_email_address_object(reply_to_addr_str) 
            #end if
        #end if
        
        if( SUBJECT in self.__map_header_options ):
            subject = self.__create_string_object_attr_type(msg_subject)
        else:
            subject = None
        
        if( IN_REPLY_TO in self.__map_header_options ):
            in_reply_to = self.__create_string_object_attr_type(msg_in_reply_to)
        else:
            in_reply_to = None
        
        if( ERRORS_TO in self.__map_header_options ):
            errors_to = self.__create_string_object_attr_type(msg_errors_to)
        else:
            errors_to = None
        
        xml_date_time = None
        if( msg_date and (DATE in self.__map_header_options) ): 
            parsedtime = email.utils.parsedate_tz(msg_date)
            xml_date_time = common.DateTimeObjectAttributeType(
                            valueOf_ = self.__get_xml_datetime_fmt(parsedtime)) 
        #end if
       

        # formatting to prevent xml invalidation
        message_id = None
        if(msg_message_id and (MESSAGE_ID in self.__map_header_options) ):
            if(msg_message_id[0] == '<'): msg_message_id = msg_message_id[1:-1]
            if(msg_message_id[-1] == '>'): msg_message_id = msg_message_id[0:-2] 
            message_id = self.__create_string_object_attr_type(msg_message_id)
    
        header_obj = email_message_object.EmailHeaderType(
                     to_addrs, cc_addrs, bcc_addrs, from_addr, subject, 
                     in_reply_to, xml_date_time, message_id, sender_addr, 
                     reply_to_addr, errors_to)

        return header_obj


    
    """ Returns a CybOX EmailOptionalHeadersType object """
    def __create_cybox_optional_headers(self, msg):
        
        (BOUNDARY, CONTENT_TYPE, MIME_VERSION, PRECEDENCE, X_MAILER, X_ORIGINATING_IP, X_PRIORITY) = ('boundary', 'content-type', 'mime-version', 'precedence', 'x-mailer', 'x-originating-ip', 'x-priority')
        
        if self.__verbose_output:
            print "** parsing optional headers"
        
        msg_boundary = msg[BOUNDARY] 
        msg_content_type = msg[CONTENT_TYPE]
        msg_mime_version = msg[MIME_VERSION]
        msg_precedence = msg[PRECEDENCE]
        msg_x_mailer = msg[X_MAILER]
        msg_x_originating_ip = msg[X_ORIGINATING_IP]
        msg_x_priority = msg[X_PRIORITY]

        if(BOUNDARY in self.__map_optional_headers_options ):
            boundary = self.__create_string_object_attr_type(msg_boundary)
        else:
            boundary = None
            
        if(CONTENT_TYPE in self.__map_optional_headers_options):
            content_type = self.__create_string_object_attr_type(msg_content_type)
        else:
            content_type = None
            
        if(MIME_VERSION in self.__map_optional_headers_options):
            mime_version = self.__create_string_object_attr_type(msg_mime_version)
        else:
            mime_version = None
        
        if(PRECEDENCE in self.__map_optional_headers_options):
            precedence = self.__create_string_object_attr_type(msg_precedence)
        else:
            precedence = None
            
        if(X_MAILER in self.__map_optional_headers_options):
            x_mailer = self.__create_string_object_attr_type(msg_x_mailer)
        else:
            x_mailer = None

        x_priority = None
        if( msg_x_priority and (X_PRIORITY in self.__map_optional_headers_options) ):
            x_priority = common.PositiveIntegerObjectAttributeType(
                               valueOf_ = int(msg_x_priority) )
        #end if
            

        x_originating_ip_addr = None
        if( msg_x_originating_ip and (X_ORIGINATING_IP in self.__map_optional_headers_options)):
            x_originating_ip_addr = self.__create_ip_address_object(msg_x_originating_ip)
        #end if


        optional_header_obj = email_message_object.EmailOptionalHeaderType(
                              boundary,content_type,mime_version,
                              precedence, x_mailer, x_originating_ip_addr,
                              x_priority)

        return optional_header_obj


    """ Creates a CybOX URIObjectType object """
    def __create_url_object(self, url):
        if not url:
            return None
        
        if( self.__verbose_output):
            print "** creating uri object for: " + url
            
        uri_obj = uri_object.URIObjectType(type_ = "URL", 
                                           Value = common.AnyURIObjectAttributeType(valueOf_ = url))
        
        uri_obj.set_anyAttributes_({'xsi:type' : 'URIObj:URIObjectType'})
        
        return uri_obj




    """ Returns a CybOX AddressType Object for use with Email addresses """
    def __create_email_address_object(self, email_addr):
        if not email_addr:
            return None

        if self.__verbose_output:
            print "** creating email address object for: " + email_addr
            
        addr_obj = address_object.AddressObjectType(
                   category = 'e-mail', 
                   Address_Value = self.__create_string_object_attr_type(email_addr))

        return addr_obj
        
        
    """ Returns a CybOX HashType object for the given md5 hash """
    def __create_hash_object(self, md5_hash):
        hash_name_type = common.HashNameType(valueOf_= "MD5")
        hash_value_type = common.SimpleHashValueType(valueOf_ = md5_hash)
        hash_type = common.HashType(Type=hash_name_type, Simple_Hash_Value=hash_value_type)
        
        return hash_type
        
        
    """ Returns a CybOX HashListType object for the given list of HashType objects """
    def __create_hash_list_object(self, list_hash_type_objects):
        hash_list_object = common.HashListType()
        
        for hash_type_object in list_hash_type_objects:
            hash_list_object.add_Hash(hash_type_object)
            
        return hash_list_object
        
    
    """ Returns a CybOX AddressType Object for use with IPv4 addresses """
    def __create_ip_address_object(self, ip_addr):
        if not ip_addr:
            return None

        if self.__verbose_output:
            print "** creating ip address object for: " + ip_addr

        addr_obj = address_object.AddressObjectType(
                   Address_Value = self.__create_string_object_attr_type(ip_addr))

        return addr_obj


    """ Returns a CybOX StringObjectAttributeType object with a value
        of @value """
    def __create_string_object_attr_type(self, value):
        if not value: 
            return None
    
        str_obj = common.StringObjectAttributeType(valueOf_ = value)
        return str_obj


    """ Returns a CybOX DateTimeObjectAttributeType object with a value
        of @value """
    def __create_date_time_object_attr_type(self, value):
        if not value:
            return None
        
        datetime_obj = common.DateTimeObjectAttributeType(valueOf_= value)
        
        return datetime_obj
        



    """ Extracts the body of the email message from the Message object.
        Multipart MIME documents can embed other multipart documents 
        within them. As a result, a depth-first approach is taken to
        finding the body segments.
        
        Each textual MIME segment which is not an attachment or header 
        is appended to a list of tuples of the form (encoding, body_text)
    """
    def __get_raw_body_text(self, msg):
        raw_body = []

        if( msg.is_multipart() == False ):
            #if self.__verbose_output:
            #    print "** message is not multipart"
            
            # text document attachments have a content type of text, so we have to filter them out
            if( (msg.has_key('content-disposition') == False) and (msg.get_content_maintype() == 'text')):
                encoding = msg['content-transfer-encoding']
                raw_body_str = msg.get_payload()
                raw_body.append((encoding, raw_body_str))
        else:
            #if self.__verbose_output:
            #    print "** message is multipart"
            
            for part in msg.get_payload():
                raw_body.extend(self.__get_raw_body_text( part ))
                    
            #end for
        #end if
        
        return raw_body


    """ Parses out URLs from the list_body_tups input and returns a map of URIObjectType objects keyed by 
        object id. Each URL in the map is unique. The input parameter, list_body_tups is a list of tuples: (encoding, body text).
        
        Regex taken from Daring Fireball: http://daringfireball.net/2010/07/improved_regex_for_matching_urls 
        and modified. The original is considered under public domain"""
    def __parse_urls(self, list_body_tups):    
        map_urls = {}
        list_observed_urls = []
        
        if(self.__verbose_output):
            print "** parsing urls from email body"
            
        url = r"""(?i)\b((?:(https?|ftp)://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))"""
        url_re = re.compile(url, re.VERBOSE | re.MULTILINE)
        
        
        for body_tup in list_body_tups: 
            encoding = body_tup[0]
            body = body_tup[1]
        
            if( (encoding) and encoding.lower() == "quoted-printable"):
                body = quopri.decodestring(body)
        
            for match in url_re.findall(body):
                found_url = match[0]            
                if found_url not in list_observed_urls:
                    url_obj = self.__create_url_object(found_url)
                    cybox_id = self.__create_cybox_id()
                    map_urls[cybox_id] = url_obj
                    list_observed_urls.append(found_url)
            
        return map_urls


    

    """ Creates a CybOX AttachmentsType object from the map_files input.
        The input map should be of the form {object_id:cybox_file_object}"""
    def __create_cybox_attachments(self, map_files):
        attachments = None
        
        if( map_files ):
            attachments = email_message_object.AttachmentsType()
            
            for file_id, f in map_files.iteritems():
                if(self.is_enabled_inline_files()):
                    attachments.add_File(f)
                else:    
                    file_obj = file_object.FileObjectType()
                    file_obj.set_anyAttributes_({'xsi:type' : 'FileObj:FileObjectType'})
                    file_obj.set_object_reference(file_id) 
                    attachments.add_File(file_obj)                    
        
        return attachments


    """ Returns a string representation of the raw email headers found within the
        input Message msg"""
    def __get_raw_headers(self, msg):
        raw_headers_str = ""
        
        for header_key_val in msg.items():
            raw_headers_str += "%s: %s\n" % (header_key_val[0], header_key_val[1])
        
        return raw_headers_str

    
    """ Adds a RelatedObjectsType object to the input CybOX Object. 
        In the context of an EmailMessageObjectType, each child object
        (objects representing attachments or urls) are related to the
        EmailMessageObject in that they are Contained_Within it.
        
        Later versions of CybOX will be amended to support the inverse
        relationship (An EmailMessageObject can point to its related
        child objects).
    """
    def __add_related_objects(self, obj, idref, obj_type):
        related_object = cybox.RelatedObjectType(idref = idref, type_ = obj_type, relationship = "Contained_Within")
        related_objects = obj.get_Related_Objects()
        if not related_objects:
            related_objects = cybox.RelatedObjectsType()
            obj.set_Related_Objects(related_objects)
            
        related_objects.add_Related_Object(related_object)



    """ Creates/returns a CybOX EmailMessageType from the given input params

        + The Email_Server element is ambiguous and ignored. I'm not
          sure how to discover the server type/name without developing
          some home-brew signature method
    """
    def __create_cybox_email_message_object(self, attachments = None, headers = None, optional_headers = None, email_server = None, raw_body = None, raw_headers = None):
        
        email_message_obj = email_message_object.EmailMessageObjectType(
                            Attachments = attachments,
                            Header = headers,
                            Optional_Header = optional_headers,
                            Email_Server = email_server,
                            Raw_Body = raw_body,
                            Raw_Header = raw_headers)

        email_message_obj.set_anyAttributes_({'xsi:type' : 'EmailMessageObj:EmailMessageObjectType'})

        return email_message_obj


    """ Generates a CybOX Oberservable Document from the input map of CybOX Objects."""
    def __create_cybox_observables(self, map_objs):    
        email_obj_map =  map_objs['message']
        file_obj_map = map_objs['files']
        url_obj_map = map_objs['urls'] 
        
        child_object_map = {}
        if self.is_enabled_include_attachments() and (not self.is_enabled_inline_files()):
            child_object_map.update(file_obj_map)
        
        if self.is_enabled_include_urls():
            child_object_map.update(url_obj_map)
        
        
        root_observable_comp = cybox.ObservableCompositionType(operator="AND")
        root_observable = cybox.ObservableType(id = self.__create_cybox_id("observable"), Observable_Composition = root_observable_comp)
        root_observables = cybox.ObservablesType(cybox_major_version = "1", cybox_minor_version= "0", Observable = [root_observable])
        
        # set up the email observable
        email_observable = cybox.ObservableType(id = self.__create_cybox_id("observable"))    
        (email_id, email_obj) = email_obj_map.iteritems().next()
        email_stateful_measure = cybox.StatefulMeasureType()
        cybox_email_obj = cybox.ObjectType(id = email_id)
        cybox_email_obj.set_Defined_Object(email_obj)
        email_stateful_measure.set_Object(cybox_email_obj)
        email_observable.set_Stateful_Measure(email_stateful_measure)
        
        map_child_observables = {}
        for obj_id, obj in child_object_map.iteritems():
            observable_id = self.__create_cybox_id("observable")
            observable = cybox.ObservableType(id = observable_id)
            cybox_object = cybox.ObjectType(id = obj_id)
            cybox_object.set_Defined_Object(obj)
            self.__add_related_objects(cybox_object, email_id, "Email Message")    
            stateful_measure = cybox.StatefulMeasureType()    
            stateful_measure.set_Object(cybox_object)
            observable.set_Stateful_Measure(stateful_measure)
            map_child_observables[obj_id] = observable
        
        for observable in map_child_observables.itervalues():
            root_observable_comp.add_Observable(observable)
        
        root_observable_comp.add_Observable(email_observable)
        
        return root_observables
  
  
    """ Parses the supplied message 
        Returns a map of message parts expressed as cybox objects.
        
        Keys: 'message', 'files', 'urls' 
    """    
    def __parse_email_message(self, msg):
        
        if(self.is_enabled_include_headers()):
            cybox_headers = self.__create_cybox_headers(msg)
        else: 
            cybox_headers = None
        
        if(self.is_enabled_include_opt_headers()):
            cybox_optional_headers = self.__create_cybox_optional_headers(msg)
        else:
            cybox_optional_headers = None
        
        if(self.is_enabled_include_attachments()):
            map_files = self.__create_cybox_files(msg)
            cybox_attachments = self.__create_cybox_attachments(map_files)
        else:
            map_files = None
            cybox_attachments = None
            
        if(self.is_enabled_include_raw_headers()):
            raw_headers_str = self.__get_raw_headers(msg)
            cybox_raw_headers = self.__create_string_object_attr_type("<![CDATA[ " + raw_headers_str + " ]]>")
        else: 
            cybox_raw_headers = None
        
        # need this for parsing urls AND raw body text
        list_raw_body = self.__get_raw_body_text(msg)
        
        if(self.is_enabled_include_raw_body()):
            raw_body_str = ""
            for raw_body_segment_tup in list_raw_body:
                raw_body_str += raw_body_segment_tup[1] + "\n"
            
            cybox_raw_body = self.__create_string_object_attr_type("<![CDATA[ " + raw_body_str.rstrip() + " ]]>" )
        else:
            cybox_raw_body = None
        
        if(self.is_enabled_include_urls()):
            map_urls = self.__parse_urls(list_raw_body)
        else:
            map_urls = None
        
        email_message_id = self.__create_cybox_id("object")
        cybox_email_message_obj =   self.__create_cybox_email_message_object( attachments = cybox_attachments,
                                                                              headers = cybox_headers,
                                                                              optional_headers = cybox_optional_headers,
                                                                              raw_body = cybox_raw_body,
                                                                              raw_headers = cybox_raw_headers )
        map_email_message = {email_message_id:cybox_email_message_obj}
 
        return {'message':map_email_message, 'files':map_files, 'urls':map_urls }
 
 
    """ Returns a CybOX Email Message Object """ 
    def generate_cybox_from_email_file(self, data):
        msg = self.__parse_email_file(data)
        map_objs = self.__parse_email_message(msg)
        observables = self.__create_cybox_observables(map_objs)
        return observables




    """ Returns a CybOX Email Message Object """
    def generate_cybox_from_email_str(self, data):
        msg = self.__parse_email_string(data)
        map_objs = self.__parse_email_message(msg)
        observables = self.__create_cybox_observables(map_objs)
        return observables




    """ Writes the CyBox Email Message Object to file """
    def write_cybox(self, cybox_obj, filename):
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
        xsi:schemaLocation="http://cybox.mitre.org/Common_v1 http://cybox.mitre.org/XMLSchema/cybox_common_types_v1.0(draft).xsd\
        http://cybox.mitre.org/objects#AddressObject http://cybox.mitre.org/XMLSchema/objects/Address/Address_Object_1.1.xsd\
        http://cybox.mitre.org/objects#FileObject http://cybox.mitre.org/XMLSchema/objects/File/File_Object_1.2.xsd\
        http://cybox.mitre.org/objects#URIObject http://cybox.mitre.org/XMLSchema/objects/URI/URI_Object_1.1.xsd\
        http://cybox.mitre.org/objects#EmailMessageObject http://cybox.mitre.org/XMLSchema/objects/Email_Message/Email_Message_Object_1.1.xsd\
        http://cybox.mitre.org/cybox_v1 http://cybox.mitre.org/XMLSchema/cybox_core_v1.0(draft).xsd"')
        

# END CLASS




def usage():
    print USAGE_TEXT
    sys.exit(EXIT_FAILURE)



def parse_header_options(arg):
    global ALLOWED_HEADER_FIELDS
    list_headers = arg.split(',')
    
    # validation
    for header in list_headers:
        if(header not in ALLOWED_HEADER_FIELDS):
            print "!! unrecoginized header field: " + header
    
    return list_headers
        


def parse_optional_header_options(arg):
    global ALLOWED_OPTIONAL_HEADER_FIELDS
    list_headers = arg.split(',')
    
    for header in list_headers:
        if(header not in ALLOWED_OPTIONAL_HEADER_FIELDS):
            print "!! unrecoginized optional header field: " + header
        
    return list_headers

    
def main():
    global VERBOSE_OUTPUT
    global ALLOWED_HEADER_FIELDS
    global ALLOWED_OPTIONAL_HEADER_FIELDS
   
    output_filename = 'output.xml'
    args = sys.argv[1:]
    input_data = None
        
    map_general_options = {}
    header_options = None
    optional_header_options = None
    
    (OPT_INLINE_FILES, OPT_RAW_BODY, 
     OPT_RAW_HEADERS, OPT_ATTACHMENTS, 
     OPT_URLS, OPT_HEADERS, OPT_OPT_HEADERS) =  ('inline-files', 'include-raw-body', 'include-raw-headers', 
                                                 'include-attachments', 'include-urls', 'include-headers', 'include-opt-headers')
        
    for i in range(0,len(args)):
        if args[i] == '-o':
            output_filename = args[i+1]
        elif args[i] == '-v':
            VERBOSE_OUTPUT = True
        elif args[i] == '-':
            input_data = sys.stdin
        elif args[i] == '-i':
            input_data = open(args[i+1], 'r')
        elif args[i] == '--headers':
            header_options = parse_header_options(args[i+1])
        elif args[i] == '--opt-headers':
            optional_header_options = parse_optional_header_options(args[i+1])
        elif args[i] == '--inline-files':
            map_general_options[OPT_INLINE_FILES] = True
        elif args[i] == '--exclude-raw-body':
            map_general_options[OPT_RAW_BODY] = False
        elif args[i] == '--exclude-raw-headers':
            map_general_options[OPT_RAW_HEADERS] = False
        elif args[i] == '--exclude-attachments':
            map_general_options[OPT_ATTACHMENTS] = False
        elif args[i] == '--exclude-urls':
            map_general_options[OPT_URLS] = False
        elif args[i] == '--exclude-opt-headers':
            map_general_options[OPT_OPT_HEADERS] = False
        elif args[i] == '-h':
            usage()
            
    if input_data is None:
        usage()
            
    try:
        translator = email_translator(VERBOSE_OUTPUT)
        
        if header_options:
            translator.set_header_options(header_options)
        if optional_header_options:
            translator.set_opt_header_options(optional_header_options)
        if(OPT_INLINE_FILES in map_general_options):
            translator.set_inline_files( map_general_options[OPT_INLINE_FILES])
        if(OPT_RAW_BODY in map_general_options):
            translator.set_include_raw_body( map_general_options[OPT_RAW_BODY])
        if(OPT_RAW_HEADERS in map_general_options):
            translator.set_include_raw_headers(map_general_options[OPT_RAW_HEADERS])
        if(OPT_ATTACHMENTS in map_general_options):
            translator.set_include_attachments(map_general_options[OPT_ATTACHMENTS])
        if(OPT_URLS in map_general_options):
            translator.set_include_urls(map_general_options[OPT_URLS])
        if(OPT_HEADERS in map_general_options):
            translator.set_include_headers(map_general_options[OPT_HEADERS])
        if(OPT_OPT_HEADERS in map_general_options):
            translator.set_include_opt_headers(map_general_options[OPT_OPT_HEADERS])
        
        cybox_objects = translator.generate_cybox_from_email_file(input_data)
        translator.write_cybox(cybox_objects, output_filename) 

    except Exception, err:
        print('\n!! error: %s\n' % str(err))
        traceback.print_exc()

       
    if(VERBOSE_OUTPUT):
        print "** processing completed" 
    
    
# entry point
if __name__ == '__main__':
    main()
    
    
__all__ = [
    "email_translator"       
    ]
