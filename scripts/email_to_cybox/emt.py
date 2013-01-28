import uuid
import cybox.bindings.cybox_common_types_1_0 as common
import cybox.bindings.cybox_core_1_0 as cybox
import cybox.bindings.email_message_object_1_2 as email_message_object
import cybox.bindings.uri_object_1_2 as uri_object
import cybox.bindings.file_object_1_3 as file_object
import cybox.bindings.address_object_1_2 as address_object


class email_translator:
    __verbose_output = False
    __email_obj_container = None
    """ Constructor """ 
    def __init__(self, verbose = False):
        self.__verbose_output = verbose
        self.__email_obj_container = self._newObjContainer(self.__create_cybox_id("object"), None)
        
    """Private class for storing new objects and their relationships"""
    class _newObjContainer:
        def __init__(self, idref, obj):
            self.idref = idref
            self.obj = obj
            self.relationships = []
            
        def add_relationship(self, idref, type_, relationship):
            self.relationships.append({'idref':idref, 'type':type_, 'relationship':relationship})
        
        def get_relationship_objects(self):
            related_objects = cybox.RelatedObjectsType()
            for r in self.relationships:
                related_object = cybox.RelatedObjectType(idref = r['idref'], type_ = r['type'], relationship = r['relationship'])
                related_objects.add_Related_Object(related_object)
            return related_objects
            
    def get_email_obj_id(self):
        return self.__email_obj_container.idref
    
    def __get_email_obj_container(self):
        return self.__email_obj_container
    
    def __add_email_obj_relationship(self, idref, type_, relationship):
        self.__email_obj_container.add_relationship(idref, type_, relationship)
    def add_email_obj_relationship(self, idref, type_, relationship):
        return self.__add_email_obj_relationship(idref, type_, relationship)
    """ Returns a unique cybox id """
    def __create_cybox_id(self, item_type = "guid"):
        return "cybox:" + item_type + "-" + str(uuid.uuid1())
    def create_cybox_id(self, item_type = "guid"):
        return self.__create_cybox_id(item_type)
    """ Returns a unique cybox id for the Email message Object"""
    def __get_email_id(self, item_type = "guid"):
        if self._EMAIL_OBJECT_ID:
            return EMAIL_OBJECT_ID
        else:
            EMAIL_OBJECT_ID = self.__create_cybox_id()
            return EMAIL_OBJECT_ID
 
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
        
        
    """ Adds a RelatedObjectsType object to the input CybOX Object. 
        In the context of an EmailMessageObjectType, each child object
        (objects representing attachments or urls) are related to the
        EmailMessageObject in that they are Contained_Within it.
        
        Later versions of CybOX will be amended to support the inverse
        relationship (An EmailMessageObject can point to its related
        child objects).
    """
    def __add_related_objects(self, obj, idref, type_, relationship="Contained Within"):
        related_object = cybox.RelatedObjectType(idref = idref, type_ = type_, relationship = relationship)
        related_objects = obj.get_Related_Objects()
        if not related_objects:
            related_objects = cybox.RelatedObjectsType()
            obj.set_Related_Objects(related_objects)
            
        related_objects.add_Related_Object(related_object)
        
        
    def __create_cybox_observable(self, obj_container):
        observable   = cybox.ObservableType(id = self.__create_cybox_id("observable"))
        cybox_object = cybox.ObjectType(id = obj_container.idref)
        cybox_object.set_Defined_Object(obj_container.obj)
        cybox_object.set_Related_Objects(obj_container.get_relationship_objects())
        stateful_measure = cybox.StatefulMeasureType()    
        stateful_measure.set_Object(cybox_object)
        observable.set_Stateful_Measure(stateful_measure)
        
        return observable
    
    """ Generates a list of cybox observables given a map of object containers """
    def __create_cybox_observable_list(self, object_map):
        list_observables = []
        for obj_id, obj_container in object_map.iteritems():
            list_observables.append(self.__create_cybox_observable(obj_container))
        
        return list_observables
    
    """ Generates a CybOX Observable Document from the input map of CybOX Objects."""
    def create_cybox_observables(self, map_objs):
        # set up the email observable
        email_observable = cybox.ObservableType(id = self.__create_cybox_id("observable"))   
        email_obj_map =  map_objs['message']
        (email_id, email_obj) = email_obj_map.iteritems().next()
        email_stateful_measure = cybox.StatefulMeasureType()
        cybox_email_obj = cybox.ObjectType(id = email_id)
        cybox_email_obj.set_Defined_Object(email_obj)
        cybox_email_obj.set_Related_Objects(self.__get_email_obj_container().get_relationship_objects())
        email_stateful_measure.set_Object(cybox_email_obj)
        email_observable.set_Stateful_Measure(email_stateful_measure)
        list_observables = [email_observable]
        root_observables = cybox.ObservablesType(cybox_major_version = "1", cybox_minor_version= "0", Observable = list_observables)
        
        if map_objs['files']:
            list_observables.extend(self.__create_cybox_observable_list(map_objs['files']))
        
        #this song and dance is so we can get the objects in the final xml in a particular order
        #we append things to list_observables in the order we want
        if map_objs['domains']:
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

    """ Writes the CyBox Email Message Object to file """
    def write_cybox(self, cybox_obj, filename):
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
        
