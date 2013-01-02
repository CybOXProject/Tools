CybOX Pattern Comparator
========================
CybOX pattern evaluation tool

Description
===========
The CybOX Pattern Comparator is a MITRE developed tool used to demonstrate the evaluation
of CybOX instance data against a CybOX pattern. 

The CybOX Pattern Comparator is under active development.

Using The CybOX Pattern Comparator
==================================
The CybOX Pattern Comparator is a python script which is designed to run on the command line.
It requires Python 2.6+ and lxml(http://lxml.de) for the parsing of XML documents and evaluation 
of XPath statements.

The CybOX Pattern Comparator provides the following arguments:
<pre>
Flags:
    -i  <input_file>       : instance data file
    -p  <input_file>       : pattern file
    -id <pattern_id>       : id of observable containing pattern
    -h                     : print help
    -v                     : verbose output
</pre>

Examples
========
<code>
$ python cybox_pattern_compare.py -i input.xml -p input_pattern.xml -id "cybox:pattern_1"

__Results__
cybox:observable_1 : True
cybox:observable_2 : False
</code>

The above invocation and results demonstrate the evaluation of input.xml against a pattern
defined within input_pattern.xml with an id of "cybox:pattern_1". The CybOX instance 
document, input.xml, contains two CybOX Observables: "cybox:observable_1" and "cybox:observable_2".
During this invocation, the instance data defined by the Observable, "cybox:observable_1"
matched the conditions defined by the CybOX Pattern, "cybox:pattern_1". The Observable,
"cybox:observable_1" evaluated to false.

Known Issues
============
Not all conditions or datatypes are handled correctly at this time. The CybOX Tools tracker
found at "https://github.com/CybOXProject/Tools/issues?labels=cybox+pattern+compare&state=open"
lists all current open issues.

Future Work
===========
The CybOX Comparator tool is under active development. Future work, features, and enhancements
are detailed within the CybOX Tools tracker found at 
"https://github.com/CybOXProject/Tools/issues?labels=&page=1&state=open"




