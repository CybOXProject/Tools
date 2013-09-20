#CybOX -> OVAL Translator
#v0.1 BETA
#Generic mappings class
#Generates OVAL tests/objects/states from a CybOX Defined Object

# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import oval57 as oval

class cybox_oval_mappings(object):
    def __init__(self):
        self.test_id_base = 0
        self.obj_id_base = 0
        self.ste_id_base = 0
        self.def_id_base = 0
        self.id_namespace = 'cybox_to_oval'
        #Mappings
        #CybOX Condition to OVAL operation mappings
        self.operator_condition_mappings = {'Equals':'equals','DoesNotEqual':'not equal','Contains':'pattern match',\
                               'GreaterThan':'greater than', 'GreaterThanOrEqual':'greater than or equal',\
                               'LessThan':'less than','LessThanOrEqual':'less than or equal','FitsPattern':'pattern match',\
                               'BitwiseAnd':'bitwise and', 'BitwiseOr':'bitwise or'}
        #CybOX Object Type to OVAL object mappings
        self.object_mappings = {'WinRegistryKeyObj:WindowsRegistryKeyObjectType':'registry_object', 'FileObj:FileObjectType':'file_object'}
        #CybOX FileObject to OVAL file_object mappings (CybOX element name : {OVAL element name, OVAL element datatype})
        self.file_object_mappings = {'File_Name':{'name':'filename','datatype':'string'},'File_Path':{'name':'path','datatype':'string'}}
        #CybOX FileObject to OVAL file_state mappings
        self.file_state_mappings = {'Size_In_Bytes':{'name':'size','datatype':'int'},'Accessed_Time':{'name':'a_time','datatype':'int'},\
                                    'Modified_Time':{'name':'m_time','datatype':'int'},'Created_Time':{'name':'c_time','datatype':'int'}}
        #CybOX WinRegistryObject to OVAL registry_object mappings
        self.registry_object_mappings = {'Key':{'name':'key','datatype':'string'},'Hive':{'name':'hive','datatype':'string'},'Name':{'name':'name','datatype':'string'}}
        #CybOX WinRegistryObject Values to OVAL registry_state mappings
        self.registry_state_mappings = {'Name':{'name':'name','datatype':'string'},'Data':{'name':'value','datatype':'string'},'Datatype':{'name':'type','datatype':'string'}}

    #Creates and returns a dictionary of OVAL test, object, and state (if applicable)
    def create_oval(self, cybox_defined_object):
        oval_entities = {}
        oval_states = []
        object_type = cybox_defined_object.xsi_type

        if object_type in self.object_mappings.keys():
            oval_object = self.create_oval_object(object_type, cybox_defined_object)
            if oval_object is not None:
                if object_type == 'WinRegistryKeyObj:WindowsRegistryKeyObjectType':
                    self.process_registry_values(cybox_defined_object, oval_object, oval_states)
                else:
                    state = self.create_oval_state(object_type, cybox_defined_object)
                    if state is not None:
                        oval_states.append(self.create_oval_state(object_type, cybox_defined_object))
                oval_test = self.create_oval_test(object_type, oval_object, oval_entities, oval_states)
                oval_entities['test'] = oval_test
                oval_entities['object'] = oval_object
                if oval_states is not None and len(oval_states) > 0:
                    oval_entities['state'] = oval_states
                return oval_entities
        else:
            return None
    
    #Create the OVAL object
    def create_oval_object(self, object_type, cybox_defined_object):
        oval_object_type = self.object_mappings.get(object_type)
        oval_object_mappings = self.object_mappings.get(object_type) + '_mappings'
        oval_object = getattr(oval,oval_object_type)(version = 1, id = self.generate_obj_id())
        for element, value in vars(cybox_defined_object).items():
            if value is not None:
                if element in getattr(getattr(self,oval_object_mappings),'keys')():
                    element_dictionary = getattr(getattr(self,oval_object_mappings),'get')(element)
                    element_name = element_dictionary.get('name')
                    element_datatype = element_dictionary.get('datatype')
                    method = 'set_' + element_name
                    getattr(oval_object,method)(oval.EntityBaseType(datatype = element_datatype, operation = self.operator_condition_mappings.get(value.get_condition()), valueOf_=value.get_valueOf_()))
        
        #Do some basic object sanity checking for certain objects
        if object_type == 'WinRegistryKeyObj:WindowsRegistryKeyObjectType' and (oval_object.hive is None or oval_object.key is None):
            return None
        return oval_object

    #Create any OVAL states
    def create_oval_state(self, object_type, cybox_defined_object):
        oval_state_type = self.object_mappings.get(object_type).split('_')[0] + '_state'
        oval_state_mappings = oval_state_type + '_mappings'
        oval_state = getattr(oval,oval_state_type)(version = 1, id = self.generate_ste_id())
        for element, value in vars(cybox_defined_object).items():
            if value is not None:
                if element in getattr(getattr(self,oval_state_mappings),'keys')():
                    element_dictionary = getattr(getattr(self,oval_state_mappings),'get')(element)
                    element_name = element_dictionary.get('name')
                    element_datatype = element_dictionary.get('datatype')
                    method = 'set_' + element_name
                    getattr(oval_state,method)(oval.EntityBaseType(datatype = element_datatype, operation = self.operator_condition_mappings.get(value.get_condition()), valueOf_=value.get_valueOf_()))
        if oval_state.hasContent_():
            return oval_state

    #Create the OVAL test
    def create_oval_test(self, object_type, oval_object, oval_entities, oval_states):
        oval_test_type = self.object_mappings.get(object_type).split('_')[0] + '_test'
        #Create the test
        comment = 'OVAL Test created from CybOX ' + object_type
        oval_test = getattr(oval,oval_test_type)(id = self.generate_test_id(), check = 'at least one', version=1.0, comment = comment)
        oval_test.set_object(oval.ObjectRefType(object_ref = oval_object.get_id()))
        if len(oval_states) > 0:
            for state in oval_states:
                if state is not None:
                    oval_test.add_state(oval.StateRefType(state_ref = state.get_id()))
        return oval_test

    #Handle any Values inside a Registry object 
    def process_registry_values(self, cybox_defined_object, oval_object, oval_states):
        #Special registry Values handling
        if cybox_defined_object.Values is not None:
            name_set = False
            for reg_value in cybox_defined_object.Values.Value:
                oval_state = oval.registry_state(version = 1, id = self.generate_ste_id())
                for element, value in vars(reg_value).items():
                    if value is not None:
                        #Corner case for handling multiple name/value pairs in the OVAL object
                        if len(cybox_defined_object.Values.Value) == 1 and not name_set:
                            if element in self.registry_object_mappings.keys():
                                oval_element = self.registry_object_mappings.get(element)
                                method = 'set_' + oval_element.get('name')
                                getattr(oval_object,method)(oval.EntityBaseType(datatype = 'string', operation = self.operator_condition_mappings.get(value.get_condition()), valueOf_=value.get_valueOf_()))
                                name_set = True
                        elif len(cybox_defined_object.Values.Value) > 1 and not name_set:
                            oval_object.set_name(oval.EntityBaseType(datatype = 'string', operation = 'pattern match', valueOf_='.*'))
                            name_set = True
                        if element in self.registry_state_mappings.keys():
                            oval_element = self.registry_state_mappings.get(element)
                            method = 'set_' + oval_element.get('name')
                            getattr(oval_state,method)(oval.EntityBaseType(datatype = 'string', operation = self.operator_condition_mappings.get(value.get_condition()), valueOf_=value.get_valueOf_()))
                if oval_state.hasContent_():
                    oval_states.append(oval_state)

    def generate_test_id(self):
        self.test_id_base += 1
        test_id = 'oval:' + self.id_namespace + ':tst:' + str(self.test_id_base)
        return test_id

    def generate_obj_id(self):
        self.obj_id_base += 1
        obj_id = 'oval:' + self.id_namespace + ':obj:' + str(self.obj_id_base)
        return obj_id

    def generate_ste_id(self):
        self.ste_id_base += 1
        ste_id = 'oval:' + self.id_namespace + ':ste:' + str(self.ste_id_base)
        return ste_id

    def generate_def_id(self):
        self.def_id_base += 1
        def_id = 'oval:' + self.id_namespace + ':def:' + str(self.def_id_base)
        return def_id
        
