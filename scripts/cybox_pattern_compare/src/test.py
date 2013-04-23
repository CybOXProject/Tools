import re
import dateutil.parser as dateparser # parses ISO 8601 dates


# BEGIN CYBOX v1.0 Conditions

CONDITION_EQUALS = 'Equals'
CONDITION_DOES_NOT_EQUAL = 'DoesNotEqual'
CONDITION_CONTAINS = 'Contains'
CONDITION_DOES_NOT_CONTAIN = 'DoesNotContain'
CONDITION_STARTS_WITH = 'StartsWith'
CONDITION_ENDS_WITH = 'EndsWith'
CONDITION_GREATER_THAN = 'GreaterThan'
CONDITION_GREATER_THAN_OR_EQUAL = 'GreaterThanOrEqual'
CONDITION_LESS_THAN = 'LessThan'
CONDITION_LESS_THAN_OR_EQUAL = 'LessThanOrEqual'
CONDITION_IS_IN_RANGE = 'IsInRange'
CONDITION_IS_NOT_IN_RANGE = 'IsNotInRange'
CONDITION_IS_IN_SET = 'IsInSet'
CONDITION_IS_NOT_IN_SET = 'IsNotInSet'
CONDITION_FITS_PATTERN = 'FitsPattern'
CONDITION_BITWISE_AND = 'BitwiseAnd'
CONDITION_BITWISE_OR = 'BitwiseOr'

# END CYBOX v1.0 Conditions

DATA_TYPES_NUMERIC = ('Int', 'Float', 'PositiveInteger', 'UnsignedInt',
                      'UnsignedLong', 'Double', 'Long', 'NonNegativeInteger')

DATA_TYPES_STRING = ('String')

DATA_TYPES_DATE  = ('DateTime')




# BEGIN CYBOX v1.0 Pattern Types
PATTERN_REGEX = 'Regex'
PATTERN_BINARY = 'Binary'
PATTERN_XPATH = "XPath"
# END CYBOX v1.0 Pattern Types


# XPATH QUERIES
XPATH_GET_OBJECT = ".//cybox:Object"
# END XPATH QUERIES

ATTR_OBJECT_REFERENCE = 'idref'
ATTR_OBJECT_DATATYPE  = 'datatype'


class Test:
    '''
    Test instances represent different methods in which CybOX objects
    can be compared, as defined by the Common::ConditionTypeEnum enumeration.
    '''
    
    def __init__(self, datatype, xpath, nsmap, expected_value, start_range=None, end_range=None):
        self.__element_datatype = datatype
        self._element_xpath = xpath
        self._xpath_nsmap = nsmap
        self._expected_value = expected_value
        self._start_range = start_range
        self._end_range = end_range
        
    def evaluate(self, doc_root, observable):
        pass
    
    
    # this will have to be changed to handle dereferencing of objects..maybe...
    def _get_container(self, doc_root, observable):
        pass
    
    
    def __run_xpath(self, _object):
        value = _object.xpath(self._element_xpath, namespaces=self._xpath_nsmap)
        
        if value is not None and len(value) > 0:
            return value[0].text
        else:
            return None
        
    
    def _get_values(self, doc_root, observable):
        list_values = []
        
        list_all_objects = observable.xpath(XPATH_GET_OBJECT, namespaces=self._xpath_nsmap)
        if list_all_objects is not None and len(list_all_objects) > 0:
            for _object in list_all_objects:
                idref = _object.get(ATTR_OBJECT_REFERENCE)
                if idref:
                    xpath_idref = "//node()[@id='" + idref + "']"
                    object_lookup = doc_root.xpath(xpath_idref)
                    if object_lookup is not None and len(object_lookup) > 0:
                        dereferenced_object = object_lookup[0]
                        value = self.__run_xpath(dereferenced_object)
                else:
                    value = self.__run_xpath(_object)
                  
                if value is not None:
                    list_values.append(value)
                    
        return list_values



class TestFactory:
    def __init__(self, xpath):
        pass

    @staticmethod
    def __check_type(datatype, condition):
        if condition == CONDITION_GREATER_THAN:
            if datatype not in DATA_TYPES_NUMERIC:
                raise Exception("!! warning: attempting to use condition: %s on non-numeric datatype: %s" % (condition, datatype) )
     
        elif condition == CONDITION_GREATER_THAN_OR_EQUAL:
            if datatype not in DATA_TYPES_NUMERIC:
                raise Exception("!! warning: attempting to use condition: %s on non-numeric datatype: %s" % (condition, datatype) )

        elif condition == CONDITION_LESS_THAN:
            if datatype not in DATA_TYPES_NUMERIC:
                raise Exception("!! warning: attempting to use condition: %s on non-numeric datatype: %s" % (condition, datatype) )
        
        elif condition == CONDITION_LESS_THAN_OR_EQUAL:
            if datatype not in DATA_TYPES_NUMERIC:
                raise Exception("!! warning: attempting to use condition: %s on non-numeric datatype: %s" % (condition, datatype) )
        
        elif condition == CONDITION_IS_IN_RANGE:
            if datatype not in DATA_TYPES_NUMERIC:
                raise Exception("!! warning: attempting to use condition: %s on non-numeric datatype: %s" % (condition, datatype) )

        elif condition == CONDITION_IS_NOT_IN_RANGE:
            if datatype not in DATA_TYPES_NUMERIC:
                raise Exception("!! warning: attempting to use condition: %s on non-numeric datatype: %s" % (condition, datatype) )
        
        elif condition == CONDITION_FITS_PATTERN:
            if datatype not in DATA_TYPES_STRING:
                print "!! warning: attempting to use condition: %s on datatype: %s" % (condition, datatype)

    @staticmethod
    def get_instance(xml_object, condition, xpath, nsmap):
        datatype = xml_object.get(ATTR_OBJECT_DATATYPE)
        
        # Sanity check on the condition and datatype
        TestFactory.__check_type(datatype, condition)
        
        if condition == CONDITION_EQUALS:
            expected_value = xml_object.text
            return TestEquals(datatype, xpath, nsmap, expected_value)

        elif condition == CONDITION_DOES_NOT_EQUAL:
            expected_value = xml_object.text
            return TestDoesNotEqual(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_CONTAINS:
            expected_value = xml_object.text
            return TestContains(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_DOES_NOT_CONTAIN:
            expected_value = xml_object.text
            return TestDoesNotContain(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_STARTS_WITH:
            expected_value = xml_object.text
            return TestStartsWith(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_ENDS_WITH:
            expected_value = xml_object.text
            return TestEndsWith(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_GREATER_THAN:
            expected_value = xml_object.text
            return TestGreaterThan(datatype, xpath, nsmap, expected_value)

        elif condition == CONDITION_GREATER_THAN_OR_EQUAL:
            expected_value = xml_object.text
            return TestGreaterThanOrEqual(datatype, xpath, nsmap, expected_value)

        elif condition == CONDITION_LESS_THAN:
            expected_value = xml_object.text
            return TestLessThan(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_LESS_THAN_OR_EQUAL:
            expected_value = xml_object.text
            return TestLessThanOrEqual(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_IS_IN_RANGE:
            expected_value = xml_object.text
            start_range = xml_object.get('start_range')
            end_range = xml_object.get('end_range')
            return TestIsInRange(datatype, xpath, nsmap, expected_value, start_range, end_range)

        elif condition == CONDITION_IS_NOT_IN_RANGE:
            expected_value = xml_object.text
            start_range = xml_object.get('start_range')
            end_range = xml_object.get('end_range')
            return TestIsNotInRange(datatype, xpath, nsmap, expected_value, start_range, end_range)

        elif condition == CONDITION_IS_IN_SET:
            expected_value = xml_object.get('value_set')
            return TestIsInSet(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_IS_NOT_IN_SET:
            expected_value = xml_object.get('value_set')
            return TestIsNotInSet(datatype, xpath, nsmap, expected_value)
        
        elif condition == CONDITION_FITS_PATTERN:
            pattern_type = xml_object.get('pattern_type')
            expected_value = xml_object.text
            
            if pattern_type == PATTERN_REGEX:
                return TestFitsRegexPattern(datatype, xpath, nsmap, expected_value)
            elif pattern_type == PATTERN_BINARY:
                return TestFitsBinaryPattern(datatype, xpath, nsmap, expected_value)
            elif pattern_type == PATTERN_XPATH:
                return TestFitsXPathPattern(datatype, xpath, nsmap, expected_value)
        


class TestTrue(Test):
    def __init__(self):
        Test.__init__(self, None, None, None, None)
        
    def evaluate(self, doc_root, observable):
        return True


class TestFalse(Test):
    def __init__(self):
        Test.__init__(self, None, None, None, None)
        
    def evaluate(self, doc_root, observable):
        return False

    
    
class TestEquals(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        if datatype in DATA_TYPES_DATE:
            datetime = dateparser.
        else: 
            return (self._expected_value in list_observable_values)
        


class TestDoesNotEqual(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        return (self._expected_value not in list_observable_values)
         
        

class TestContains(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if self._expected_value in value:
                return True
        return False


class TestDoesNotContain(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if self._expected_value in value:
                return False
        return True

        
class TestStartsWith(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if value.startswith(self._expected_value):
                return True
        return False
        
        
 
class TestEndsWith(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if value.endswith(self._expected_value):
                return True
        return False
        
     

class TestGreaterThan(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if (int(value) > int(self._expected_value)):
                return True
        return False
        
        
        

class TestGreaterThanOrEqual(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if (int(value) >= int(self._expected_value)):
                return True
        return False
        
        
        
class TestLessThan(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if (int(value) < int(self._expected_value)):
                return True
        return False
             
        
        
class TestLessThanOrEqual(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if (int(value) <= int(self._expected_value)):
                return True
        return False
        
        
        
        
class TestIsInRange(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value, start_range, end_range):
        Test.__init__(self, datatype, xpath, nsmap, expected_value, start_range, end_range)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if  ((int(self._start_range) <= int(value)) and (int(self._end_range) >= int(value))):
                return True
        return False
        
        
class TestIsNotInRange(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value, start_range, end_range):
        Test.__init__(self, datatype, xpath, nsmap, expected_value, start_range, end_range)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if  ((int(self._start_range) <= int(value)) and (int(self._end_range) >= int(value))):
                return False
        return True
        
        
        
class TestIsInSet(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        self._expected_value = expected_value.split(',')
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if value in self._expected_value:
                return True
        return False
        

        
class TestIsNotInSet(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        self._expected_value = expected_value.split(',')
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if value in self._expected_value:
                return False
        return True
        



class TestFitsRegexPattern(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        self.__pattern = re.compile(expected_value)
        
    def evaluate(self, doc_root, observable):
        list_observable_values = self._get_values(doc_root, observable)
        
        for value in list_observable_values:
            if (self.__pattern.match(value) is not None):
                return True
        return False
    

class TestFitsXPathPattern(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        print "!! xpath pattern test not evaluated"
        return False
        


class TestFitsBinaryPattern(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        print "!! binary pattern test not evaluated"
        return False



class TestBitwiseAnd(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        print "!! bitwiseand test not evaluated"
        return False



class TestBitwiseOr(Test):
    def __init__(self, datatype, xpath, nsmap, expected_value):
        Test.__init__(self, datatype, xpath, nsmap, expected_value)
        
    def evaluate(self, doc_root, observable):
        print "!! bitwiseor test not evaluated"
        return False


