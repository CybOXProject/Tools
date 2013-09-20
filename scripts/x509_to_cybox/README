****************************************************

 X509 Certificate -> CybOX XML Converter Script

 Copyright (c) 2013 - The MITRE Corporation
 All rights reserved. See LICENSE.txt for complete terms.

****************************************************

BY USING THE X509 TO CYBOX SCRIPT, YOU SIGNIFY YOUR ACCEPTANCE OF THE TERMS AND 
CONDITIONS OF USE.  IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THIS SCRIPT.

#################################################################
#Generates CybOX Output from an X509 Certificate txt file       #
#Compatible with CybOX v2.0.1                                   #
#                                                               #
#v0.2 - BETA                                                    #
#06/18/2013                                                     #
#                                                               #
#################################################################
# CybOX - http://cybox.mitre.org                                #
#################################################################
--------------------------------------------------------------------------------
--Installation Notes------------------------------------------------------------

Extract included files into your directory of choice. This script is dependent on the following libraries:

+ python-cybox v2.0.1.x

Install python-cybox with the following command:
$ pip install cybox

This script was created using Python 2.7.x, and so may not be compatible with 3.0.x.
--------------------------------------------------------------------------------
--Included Files----------------------------------------------------------------

README: this file.
x509_to_cybox.py: the X509 to CybOX XML Python converter script.
terms.txt: the terms of use for this script.
\example: a folder with an example input/output.
--------------------------------------------------------------------------------
--Usage Notes-------------------------------------------------------------------
This script supports the parsing and conversion of one or more X509 certificates
captured in a linefeed ('\n') delimited text file into CybOX. A single Observable
will be created for each certificate.

There are two main command line parameters for this script:

-i: the path to the input X509 certificate text file

-o: the path to the output CybOX XML file

To use the script, run the following command:

python x509_to_cybox.py -i <x509 certificate text file> -o <cybox xml file>

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
