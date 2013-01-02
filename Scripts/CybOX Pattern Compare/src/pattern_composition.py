'''
Created on Jul 17, 2012

@author: BWORRELL
'''

import lxml.etree as etree
import test


NSMAP={
       'cybox':'http://cybox.mitre.org/cybox_v1',
       'common':'http://cybox.mitre.org/Common_v1',
       'xsl':'http://www.w3.org/1999/XSL/Transform',
       'xsi':'http://www.w3.org/2001/XMLSchema-instance'
       }


ATTR_XSI_TYPE = '{http://www.w3.org/2001/XMLSchema-instance}type'
ATTR_OPERATOR = 'operator'
ATTR_ID = 'id'
ATTR_OBJECT_REFERENCE = 'idref'
ATTR_CONDITION = 'condition'

TAG_STATEFUL_MEASURE = 'StateFul_Measure'
TAG_OBSERVABLE_COMPOSITION = 'Observable_Composition'

XPATH_OBS_COMPOSITION = "./cybox:Observable_Composition"
XPATH_OBS_STATEFUL_MEASURE = "./cybox:Stateful_Measure"
XPATH_OBS_OBJECT = "./cybox:Stateful_Measure/cybox:Object"
XPATH_OBJ_DEFINED_OBJECT = "./cybox:Defined_Object"
XPATH_OBJ_CONDITION = ".//node()[@condition]"
XPATH_OBJ_LOCAL_NAME = "local-name(.)"



class PatternComposition():
    '''
        Compositions are logical structures representing patterns described by tests and/or other
        compositions.
    '''
    
    (OPERATOR_AND, OPERATOR_OR) = ('AND', 'OR')    
    
   
    
    def __init__(self):
        self.__object_type = None
        self.__list_tests = []
        self.__list_compositions = []
        self.__operator = 'AND'
        self.__verbose_output = False
    
    
    def set_verbose_output(self, verbose):
        self.__verbose_output = verbose
    
    
    
    def set_operator(self, op):
        if op in (self.OPERATOR_AND, self.OPERATOR_OR):
            self.__operator = op
        else:
            raise Exception, 'operator ' + op + " not recognized"
    
    

    def __evaluate_tests(self, doc_root, observable_root, include_match_scores = False):
        """
        Tests are always going to be evaluated against a single instance of 
        observable and object, and as such, the operator will always be 'AND'.
        Because of this, we can stop evaluating the moment a test returns False.
        """
                
        is_measure = observable_root.xpath(XPATH_OBS_STATEFUL_MEASURE, namespaces=NSMAP)
        if is_measure:
            list_observables = [observable_root]
        else:
            xpath_observables = ".//cybox:Observable[cybox:Stateful_Measure/cybox:Object/cybox:Defined_Object/@xsi:type='%s']" % (self.__object_type)
            list_observables = observable_root.xpath(xpath_observables, namespaces=NSMAP)
        
        if list_observables is not None and len(list_observables) > 0:
            for observable in list_observables:
                for test in self.__list_tests:
                    result = test.evaluate(doc_root, observable)
                    if not result:
                        return False
        else:
            return False
        
        return True
        
    
    
    def evaluate(self, doc_root, observable_root, include_match_scores = False):
        results = []
        
        if not self.__list_compositions and not self.__list_tests:
            return True
        
        if len(self.__list_tests) > 0:
            test_result = self.__evaluate_tests(doc_root, observable_root)
            results.append(test_result)
            
        for comp in self.__list_compositions:
            result = comp.evaluate(doc_root, observable_root)
            results.append(result)
            
        if( self.__operator == PatternComposition.OPERATOR_AND ):
            return (False not in results)
        elif (self.__operator == PatternComposition.OPERATOR_OR):
            return (True in results)
        else:
            raise Exception("unknown composition operator: " + self.__operator)
            
            

    def __parse_operator(self, observable_composition):
        operator = observable_composition.get(ATTR_OPERATOR)
        if not operator:
            operator = self.OPERATOR_AND
        return operator



    def __create_tests(self, defined_object, datatype):
        list_tests = []
        
        if defined_object is not None:
            list_conditions = defined_object.xpath(XPATH_OBJ_CONDITION, namespaces=NSMAP)
            if list_conditions:
                root_type = defined_object.get(ATTR_XSI_TYPE)
                test_xpath_start = "./cybox:Defined_Object[@xsi:type = '" + root_type + "']"
                
                for conditional_object in list_conditions:
                    xpath = ""
                    condition_ns_map = conditional_object.nsmap
                    condition_value = conditional_object.get(ATTR_CONDITION)
                    
                    node = conditional_object
                    while node.tag != '{http://cybox.mitre.org/cybox_v1}Defined_Object':
                        #node.tag contains namespace info, so we'll use the 
                        #xpath local-name() function
                        qname = etree.QName(node.tag)
                        localname = qname.localname
                        prefix = node.prefix
                        xpath = "/" + prefix + ":" + localname + xpath
                        node = node.getparent()
                    
                    xpath = test_xpath_start + xpath
                    test_instance = test.TestFactory.get_instance(conditional_object, condition_value, xpath, condition_ns_map)
                    list_tests.append(test_instance)
        
        return list_tests
                    
    
    
    '''
        Returns the object found within the stateful_measure of the
        given observable. If the object returned from the stateful
        measure contains an idref, return the dereferenced object
    '''
    def __get_object(self, root, observable):
        rtn_val = None
        
        _object = observable.xpath(XPATH_OBS_OBJECT, namespaces=NSMAP)
        if _object:  
            idref = _object[0].get(ATTR_OBJECT_REFERENCE)
            # does this _object reference another elsewhere?
            if idref:
                xpath_idref = "//node()[@id='" + idref + "']"
                dereferenced_object = root.xpath(xpath_idref, namespaces=NSMAP)
                
                if dereferenced_object:
                    rtn_val = dereferenced_object[0]
            else:
                rtn_val = _object[0]
                
        
        return rtn_val


    '''
        Given an observable that contains a stateful_measure,
        this returns a Test object representing the condition
        of the defined_object contained within the observable.
    '''
    def __parse_tests(self, root, observable):
        list_tests = []
        _object = self.__get_object(root, observable)
        
        if _object is not None:
            defined_object = _object.xpath(XPATH_OBJ_DEFINED_OBJECT, namespaces=NSMAP)
            if defined_object:
                datatype = defined_object[0].get(ATTR_XSI_TYPE)
                tests = self.__create_tests(defined_object[0], datatype)
                list_tests.extend(tests)
            
            else:
                print "!! cybox:Defined_Object not found within Stateful_Measure::Object skipping"
                list_tests.append(test.TestTrue())
            
        else:
            print "!! cybox:Object not found within Stateful_Measure: skipping"
            list_tests.append(test.TestTrue())
            
        return (datatype, list_tests)


           
    def parse(self, doc_root, observable):
        obs_comp = observable.xpath(XPATH_OBS_COMPOSITION, namespaces=NSMAP)
        if obs_comp:
            operator = self.__parse_operator(obs_comp[0])
            self.__operator = operator
                    
            for obs in obs_comp[0].getchildren():
                pattern_comp = PatternComposition()
                pattern_comp.parse(doc_root, obs)
                self.__list_compositions.append(pattern_comp)
        
        elif observable.xpath(XPATH_OBS_STATEFUL_MEASURE, namespaces=NSMAP):
            (datatype, list_tests) = self.__parse_tests(doc_root, observable)
            self.__list_tests.extend(list_tests)
            self.__object_type = datatype
        
        
        else:
            print '** parse(): observable contains neither STATEFUL_MEASURE nor OBSERVABLE_COMPOSITION: skipping ' + observable.get(ATTR_ID)
        
        
        
        
        
        
        
        
        
        