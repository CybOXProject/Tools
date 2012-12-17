#!/usr/bin/python 


import sys
import traceback

import lxml.etree as etree
from pattern_composition import PatternComposition

# BEGIN GLOBAL VARIABLES
USAGE_TEXT = """
CybOX Pattern Utility
v0.1 BETA // Compatible with CybOX v1.0

Evaluates a CybOX Observables Document by comparing
contained Observables to an input CybOX Pattern.

Usage: python cybox_pattern_compare.py <flags>
Flags:
    -i  <input_file>       : instance data file
    -p  <input_file>       : pattern file 
    -id <pattern_id>       : id of observable containing pattern
    -h                     : print help
    -v                     : verbose output
    
Example: `python cybox_pattern_compare -i input.xml -p pattern.xml -id cybox:pattern-1`
"""

VERBOSE_OUTPUT = False
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

NS={
    'cybox':'http://cybox.mitre.org/cybox_v1',
    'common':'http://cybox.mitre.org/Common_v1',
    'xsl':'http://www.w3.org/1999/XSL/Transform',
    'xsi':'http://www.w3.org/2001/XMLSchema-instance'
    }

ATTR_XSI_TYPE = '{http://www.w3.org/2001/XMLSchema-instance}type'
ATTR_ID = 'id'

# END GLOBAL VARIABLES


def find_matches(input_instance, input_pattern, pattern_id):
    map_results = {}
    xpath_pattern = "//cybox:Observable[@id='" + pattern_id + "']"
    xpath_observables = "./cybox:Observable"

    if VERBOSE_OUTPUT:
        print "** parsing pattern"
    
    pattern_root = etree.parse(input_pattern)
    list_pattern_observables = pattern_root.xpath(xpath_pattern, namespaces=NS)
    
    if list_pattern_observables is not None and len(list_pattern_observables) > 0:
        pattern_observable = list_pattern_observables[0]
        pattern_composition = PatternComposition()
        pattern_composition.parse(pattern_root, pattern_observable)
    else:
        raise Exception("Unable to find observable with id: " + pattern_id)
    
    if VERBOSE_OUTPUT: 
        print "** parsing instance document"
    
    instance_root = etree.parse(input_instance)
    list_instance_observables = instance_root.xpath(xpath_observables, namespaces=NS)
    
    if list_instance_observables is not None:
        for instance_observable in list_instance_observables:
            instance_id = instance_observable.get(ATTR_ID)
            
            if VERBOSE_OUTPUT:
                print "** evaluating observable with id: %s" % (instance_id)
            
            match = pattern_composition.evaluate(instance_root, instance_observable)
            map_results[instance_id] = match
            
    return map_results
            
    

def print_results(map_results):
    print ""
    print "__Results__"
    
    for _id, result in map_results.iteritems():
        print "%s : %s" % (_id, result)

    print ""


def usage():
    print USAGE_TEXT
    sys.exit(EXIT_FAILURE)



def main():
    global VERBOSE_OUTPUT
    args = sys.argv[1:]
    input_pattern = None
    input_instance = None
    pattern_id = None
        
    for i in range(0,len(args)):
        if args[i] == '-v':
            VERBOSE_OUTPUT = True
        elif args[i] == '-i':
            input_instance = open(args[i+1], 'rb')
        elif args[i] == '-p':
            input_pattern = open(args[i+1], 'rb')
        elif args[i] == '-id':
            pattern_id = args[i+1]
        elif args[i] == '-h':
            usage()
            
    if None in (input_pattern, input_instance, pattern_id):
        usage()
            
    try:
        map_results = find_matches(input_instance, input_pattern, pattern_id)
        print_results(map_results)
       
    except Exception, err:
        print('\n!! error: %s\n' % str(err))
        traceback.print_exc()
       
    if(VERBOSE_OUTPUT):
        print "** processing completed" 
    
    
# entry point
if __name__ == '__main__':
    main()
    
    
__all__ = [
    "find_matches"
    ]





