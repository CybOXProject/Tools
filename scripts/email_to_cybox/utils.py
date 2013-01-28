#cybox bindings
import cybox.bindings.cybox_common_types_1_0 as common
import cybox.bindings.cybox_core_1_0 as cybox
import cybox.bindings.email_message_object_1_2 as email_message_object
import cybox.bindings.uri_object_1_2 as uri_object
import cybox.bindings.file_object_1_3 as file_object
import cybox.bindings.address_object_1_2 as address_object
import uuid

class LM_CybOX_Helper():
    def __init__(self):
        pass
    
    def create_email_address_object(self, email_addr):
        if not email_addr:
            return None
        addr_obj = address_object.AddressObjectType(
                   category = 'e-mail', 
                   Address_Value = self.create_string_object_attr_type(email_addr))
        return addr_obj
    def create_url_object(self, url):
        if not url:
            return None
        uri_obj = uri_object.URIObjectType(type_ = "URL", 
                                           Value = common.AnyURIObjectAttributeType(valueOf_ = url))
        uri_obj.set_anyAttributes_({'xsi:type' : 'URIObj:URIObjectType'})
        
        return uri_obj
    
    def create_string_object_attr_type(self, value):
        if not value: 
            return None
        str_obj = common.StringObjectAttributeType(valueOf_ = value)
        return str_obj
    def create_domain_name_object(self, domain):
        if not domain:
            return None
        uri_obj = uri_object.URIObjectType(type_ = "Domain Name", 
                                           Value = common.AnyURIObjectAttributeType(valueOf_ = domain))
        uri_obj.set_anyAttributes_({'xsi:type' : 'URIObj:URIObjectType'})
        return uri_obj
    def create_hash_object(self, hash_value, hash_type):
        hash_name_type = common.HashNameType(valueOf_= hash_type)
        hash_value_type = common.SimpleHashValueType(valueOf_ = hash_value)
        hash_type = common.HashType(Type=hash_name_type, Simple_Hash_Value=hash_value_type)
        
        return hash_type
    def create_hash_list_object(self, list_hash_type_objects):
        hash_list_object = common.HashListType()
        
        for hash_type_object in list_hash_type_objects:
            hash_list_object.add_Hash(hash_type_object)
            
        return hash_list_object
    def create_date_time_object_attr_type(self, value):
        if not value:
            return None
        datetime_obj = common.DateTimeObjectAttributeType(valueOf_= value)
        return datetime_obj
    def create_date_object_attr_type(self, value):
        if not value:
            return None
        date_obj = common.DateObjectAttributeType(valueOf_= value)
        return date_obj
    def create_hex_binary_object_attr_type(self, value):
        if not value:
            return None        
        hex_obj = common.HexBinaryObjectAttributeType(valueOf_= value)
        return hex_obj
    def create_cybox_email_message_object(self, attachments = None, links = None, headers = None, optional_headers = None, email_server = None, raw_body = None, raw_headers = None):
        
        email_message_obj = email_message_object.EmailMessageObjectType(
                            Attachments = attachments,
                            Links = links,
                            Header = headers,
                            Optional_Header = optional_headers,
                            Email_Server = email_server,
                            Raw_Body = raw_body,
                            Raw_Header = raw_headers)
    
        email_message_obj.set_anyAttributes_({'xsi:type' : 'EmailMessageObj:EmailMessageObjectType'})
    
        return email_message_obj
    
    def create_cybox_files(self, translator, children, parentID, parent_type="Email Message"):
        map_level_1_file_objs = {}
        map_file_objs = {}
        
        for part in children:
            # if it's an attachment-type, pull out the filename
            # and calculate the size in bytes
            filename  = part['cybox_filename']
            file_size = part['cybox_file_size']
            md5_hash  = part['cybox_md5_hash']
            sha256    = part['cybox_sha256']
            ssdeep    = part['cybox_ssdeep']
            
            size_in_bytes = common.UnsignedLongObjectAttributeType(
                            valueOf_ = str(file_size))
            modified_date = None
            created_date  = None
            extension     = None
            
            cybox_id = translator.create_cybox_id("object")
            
            hash_type_obj0 = self.create_hash_object(md5_hash, "MD5")
            hash_type_obj1 = self.create_hash_object(sha256,   "SHA256")
            hash_type_obj2 = self.create_hash_object(ssdeep,   "ssdeep")
            
            hashes = [] 
            hashes.append(hash_type_obj0)
            hashes.append(hash_type_obj1)
            hashes.append(hash_type_obj2)
            
            file_obj = file_object.FileObjectType(
                       File_Name      = self.create_string_object_attr_type(filename),
                       File_Extension = self.create_string_object_attr_type(extension),
                       Size_In_Bytes  = size_in_bytes,
                       Hashes         = self.create_hash_list_object(hashes),
                       Modified_Time  = self.create_string_object_attr_type(modified_date),
                       Created_Time   = self.create_date_time_object_attr_type(created_date))
            
            file_obj.set_anyAttributes_({'xsi:type' : 'FileObj:FileObjectType'})
            file_obj_container = translator._newObjContainer(cybox_id,file_obj)
            file_obj_container.add_relationship(parentID,parent_type,'Contained_Within')
            if parent_type == "Email Message":
                translator.add_email_obj_relationship(cybox_id, 'File', 'Contains')
                map_level_1_file_objs[cybox_id] = file_obj_container
            map_file_objs[cybox_id] = file_obj_container
            (next_level, newfiles)  = self.create_cybox_files(translator, part['cybox_subfiles'], cybox_id, "File")
            for file_id, f in newfiles.iteritems():
                map_file_objs[file_id] = f
        # end for
        return map_level_1_file_objs, map_file_objs
    def create_cybox_attachments(self, map_files, inline_attachments=False):
        attachments = None
        if( map_files ):
            attachments = email_message_object.AttachmentsType()
            for file_id, f in map_files.iteritems():
                if inline_attachments:
                    attachments.add_File(f.obj)
                file_obj = file_object.FileObjectType()
                file_obj.set_anyAttributes_({'xsi:type' : 'FileObj:FileObjectType'})
                file_obj.set_object_reference(file_id) 
                attachments.add_File(file_obj)
        return attachments
    def create_ip_address_object(self, ip_addr):
        if not ip_addr:
            return None
        if ':' in str(ip_addr):
            category = 'ipv6-addr'
        else:
            category = 'ipv4-addr'
            
        addr_obj = address_object.AddressObjectType(
                   Address_Value = self.create_string_object_attr_type(ip_addr),
                   category = category)
        addr_obj.set_anyAttributes_({'xsi:type' : 'AddressObj:AddressObjectType'})
        return addr_obj
    
    def create_cybox_id(self, item_type = "guid"):
        return "cybox:" + item_type + "-" + str(uuid.uuid1())
