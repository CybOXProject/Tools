# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See TERMS.txt for complete terms.

#X509 Certificate -> CybOX Observables Script
#v0.2 **BETA**
#https://github.com/CybOXProject/Tools for latest version

import sys
import os
import cybox
from cybox.core import Observables, Observable, Object
from cybox.utils.nsparser import Namespace

#Supported X509 Keywords
x509_keywords = ['Version', 'Serial Number', 'Signature Algorithm', 'Issuer', 'Not Before', 'Not After ', 'Subject',
                 'Subject Public Key Info', 'Public Key Algorithm', 'RSA Public-Key', 'Public-Key', 'Modulus',
                 'RSA Public Key', 'Modulus (512 bit)', 'Modulus (1024 bit)', 'Modulus (2048 bit)', 'Exponent', 
                 'X509v3 Basic Constraints', 'X509v3 Name Constraints', 'X509v3 Policy Constraints', 'X509v3 Subject Alternative Name',
                 'X509v3 Issuer Alternative Name', 'X509v3 Subject Directory Attributes', 'X509v3 CRL Distribution Points',
                 'X509v3 Private Key Usage Period','X509v3 Certificate Policies', 'X509v3 Policy Mappings',
                 'X509v3 Subject Key Identifier', 'X509v3 Authority Key Identifier', 'Netscape Comment',
                 'Netscape Certificate Type', 'Netscape Cert Type', 'X509v3 Key Usage', 'X509v3 Extended Key Usage', 
                 '2.5.29.1', '2.5.29.2']
#Ignored X509 Keywords
ignored_keywords = ['X509v3 extensions', 'Validity', '-----BEGIN CERTIFICATE-----', '-----END CERTIFICATE-----']

def cert_to_cybox(cert_dict):
    'Parse the certificate dictionary and create the CybOX Observable representation from it'
    properties_dict = {'xsi:type' : 'X509CertificateObjectType'}
    properties_dict['certificate'] = {}
    properties_dict['certificate_signature'] = {}
    properties_dict['certificate']['subject_public_key'] = {}
    properties_dict['certificate']['validity'] = {}
    properties_dict['certificate']['standard_extensions'] = {}
    properties_dict['certificate']['non_standard_extensions'] = {}
    properties_dict['certificate']['subject_public_key']['rsa_public_key'] = {}
    x509_obj_dict = {'properties' : properties_dict} 
    x509_to_cybox = Namespace("https://github.com/CybOXProject/Tools", "x509_to_cybox")
    observable_dict = {'id': cybox.utils.IDGenerator(x509_to_cybox).create_id(prefix="observable"), 'object' : x509_obj_dict}

    for key, value in cert_dict.items():
        if key == 'Version' :
            split_version = value.split(' ')
            properties_dict['certificate']['version'] = split_version[0]
        elif key == 'Serial Number':
            properties_dict['certificate']['serial_number'] = value
        elif key == 'Subject':
            properties_dict['certificate']['subject'] = value
        elif key == 'Issuer':
            properties_dict['certificate']['issuer'] = value
        elif key == 'Signature Algorithm':
            properties_dict['certificate']['signature_algorithm'] = value
        elif key == 'Public Key Algorithm':
            properties_dict['certificate']['subject_public_key']['public_key_algorithm'] = value
        elif key == 'Modulus' or key == 'Modulus (2048 bit)' or key == 'Modulus (1024 bit)' or key == 'Modulus (512 bit)':
            properties_dict['certificate']['subject_public_key']['rsa_public_key']['modulus'] = value
        elif key == 'Exponent':
            split_exponent = value.split(' ')
            properties_dict['certificate']['subject_public_key']['rsa_public_key']['exponent'] = split_exponent[0]
        elif key == 'Not Before' : 
            properties_dict['certificate']['validity']['not_before'] = value
        elif key == 'Not After' : 
            properties_dict['certificate']['validity']['not_after'] = value
        elif key == 'Signature Algorithm_':
            split_signature = value.split(' ')
            if len(split_signature) == 2:
                properties_dict['certificate_signature']['signature_algorithm'] = split_signature[0]
                properties_dict['certificate_signature']['signature'] = split_signature[1]
            else:
                properties_dict['certificate_signature']['signature'] = value
        elif key == 'X509v3 Basic Constraints':
            properties_dict['certificate']['standard_extensions']['basic_constraints'] = value
        elif key == 'X509v3 Name Constraints':
            properties_dict['certificate']['standard_extensions']['name_constraints'] = value
        elif key == 'X509v3 Policy Constraints':
            properties_dict['certificate']['standard_extensions']['policy_constraints'] = value
        elif key == 'X509v3 Subject Key Identifier':
            properties_dict['certificate']['standard_extensions']['subject_key_identifier'] = value
        elif key == 'X509v3 Authority Key Identifier':
            properties_dict['certificate']['standard_extensions']['authority_key_identifier'] = value
        elif key == 'X509v3 Subject Alternative Name':
            properties_dict['certificate']['standard_extensions']['subject_alternative_name'] = value
        elif key == 'X509v3 Issuer Alternative Name':
            properties_dict['certificate']['standard_extensions']['issuer_alternative_name'] = value
        elif key == 'X509v3 Subject Directory Attributes':
            properties_dict['certificate']['standard_extensions']['subject_directory_attributes'] = value
        elif key == 'X509v3 CRL Distribution Points':
            properties_dict['certificate']['standard_extensions']['crl_distribution_points'] = value
        elif key == 'X509v3 Inhibit Any Policy':
            properties_dict['certificate']['standard_extensions']['inhibit_any_policy'] = value
        elif key == 'X509v3 Private Key Usage Period':
            properties_dict['certificate']['standard_extensions']['private_key_usage_period'] = value
        elif key == 'X509v3 Certificate Policies':
            properties_dict['certificate']['standard_extensions']['certificate_policies'] = value
        elif key == 'X509v3 Policy Mappings':
            properties_dict['certificate']['standard_extensions']['policy_mappings'] = value
        elif key == 'X509v3 Key Usage':
            properties_dict['certificate']['standard_extensions']['key_usage'] = value
        elif key == 'X509v3 Extended Key Usage':
            properties_dict['certificate']['standard_extensions']['extended_key_usage'] = value
        elif key == 'Netscape Comment':
            properties_dict['certificate']['non_standard_extensions']['netscape_comment'] = value
        elif key == 'Netscape Cert Type' or key == 'Netscape Certificate Type':
            properties_dict['certificate']['non_standard_extensions']['netscape_certificate_type'] = value
        elif key == '2.5.29.1':
            properties_dict['certificate']['non_standard_extensions']['old_authority_key_identifier'] = value
        elif key == '2.5.29.2':
            properties_dict['certificate']['non_standard_extensions']['old_primary_key_attributes'] = value
    return Observable.from_dict(observable_dict)

def normalize_datetime(x509_datetime):
    '''Normalize the x509 datetime into the xs:datetime format'''
    split_datetime = x509_datetime.split(' ')
    month = split_datetime[0]
    day = split_datetime[1]
    time = split_datetime[2]
    year = split_datetime[3]

    if len(day) == 1:
        day = '0' + day

    return year + '-' + month_to_int(month) + '-' + day + 'T' + time

def month_to_int(month):
    '''Simple month to integer conversion'''
    if 'Jan' in month:
        return '01'
    elif 'Feb' in month:
        return '02'
    elif 'Mar' in month:
        return '03'
    elif 'Apr' in month:
        return '04'
    elif 'May' in month:
        return '05'
    elif 'Jun' in month:
        return '06'
    elif 'Jul' in month:
        return '07'
    elif 'Aug' in month:
        return '08'
    elif 'Sep' in month:
        return '09'
    elif 'Oct' in month:
        return '10'
    elif 'Nov' in month:
        return '11'
    elif 'Dec' in month:
        return '12'

def tokenize_input(cert_array):
    '''Breakup the certificate array into its Python dictionary representation'''
    cert_dict = {}
    current_index = 0

    while(current_index < len(cert_array)):
        current_line = cert_array[current_index]

        if current_index < len(cert_array)-1:
            next_line = cert_array[current_index+1]

        if keyword_test(current_line):
            split_line = current_line.lstrip().strip('\n').split(':',1)
            current_keyword = split_line[0]
            
            if keyword_test(next_line) or ignored_keyword_test(next_line):
                if len(split_line[1]) > 0:
                    if not cert_dict.has_key(current_keyword.strip()):
                        cert_dict[current_keyword.strip()] = split_line[1].lstrip().rstrip()
                    else:
                        cert_dict[current_keyword.strip() + '_'] = split_line[1].lstrip().rstrip()
                    current_index += 1
                else:
                    current_index += 1
            else:
                if len(split_line[1].lstrip()) > 0:
                    current_data = split_line[1].lstrip().rstrip() + ' '
                else:
                    current_data = ''
                counter = 1
                while(not keyword_test(cert_array[current_index + counter]) and not ignored_keyword_test(cert_array[current_index + counter])):
                    current_data += cert_array[current_index + counter].lstrip().strip('\n').rstrip()
                    if current_index + counter < len(cert_array) - 1:
                        counter += 1
                    else: break
                if not cert_dict.has_key(current_keyword): 
                    cert_dict[current_keyword] = current_data
                else:
                    cert_dict[current_keyword + '_'] = current_data
                current_index += counter
        else:
            current_index += 1
                    
    return cert_dict

def split_certs(raw_lines):
    '''#Split up the multiple Certificates that may be found in the input file'''
    certs = []
    current_lines = []
    current_cert = False
    for line in raw_lines:
        if 'Certificate:' in line and not current_cert:
            current_cert = True
            continue
        elif 'Certificate:' in line and current_cert:
            certs.append(current_lines)
            current_lines = []

        if current_cert:
            current_lines.append(line)
            if raw_lines.index(line) == len(raw_lines) - 1:
                certs.append(current_lines)
                return certs
    return certs
            
def keyword_test(line):
    '''Test a line for an X509 keyword'''
    for x509_keyword in x509_keywords:
        if line.lstrip().startswith((x509_keyword + ':')):
            return True
    return False

def ignored_keyword_test(line):
    '''Test a line for an ignored keyword'''
    for ignored_keyword in ignored_keywords:
        if line.lstrip().startswith((ignored_keyword)):
            return True
    return False

def get_input(infilename):
    '''Read in an input file and return and array of lines read'''
    return open(infilename, 'r').readlines()

#Print the usage text    
def usage():
    print USAGE_TEXT
    sys.exit(1)
    
USAGE_TEXT = """
X509 Certificate --> CybOX XML Converter Utility
v0.2 BETA // Compatible with CybOX v2.0

Usage: python openioc_to_cybox.py -i <x509 cert txt file> -o <cybox xml file>
"""

def main():
    infilename = ''
    outfilename = ''

    #Get the command-line arguments
    args = sys.argv[1:]
    
    #Basic argument checking
    if len(args) < 4:
        usage()
        sys.exit(1)
        
    for i in range(0,len(args)):
        if args[i] == '-i':
            infilename = args[i+1]
        elif args[i] == '-o':
            outfilename = args[i+1]
     #Basic input file checking
    if os.path.isfile(infilename):
        #Get the raw lines from the input file
        raw_lines = get_input(infilename)
        #Breakup each certificate into its corresponding lines
        cert_strings = split_certs(raw_lines)
        observables_list = []
        #Process each certificate array into its CybOX representation
        for cert_array in cert_strings:
            #Get the Python dictionary corresponding to the certificate
            cert_dict = tokenize_input(cert_array)
            observables_list.append(cert_to_cybox(cert_dict))

        observables = Observables(observables_list)
        #Open the output file for writing and write out the generated Observables
        out_file = open(outfilename, 'w')
        out_file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        out_file.write("<!-- Generated by X509 to CybOX Utility\nhttps://github.com/CybOXProject/Tools/-->\n")
        out_file.write("<!DOCTYPE doc [<!ENTITY comma '&#44;'>]>\n")
        out_file.write(observables.to_xml(False, ['xmlns:x509_to_cybox="https://github.com/CybOXProject/Tools"']))
        out_file.close()
    else:
        print('\nError: Input file not found or inaccessible.')
        sys.exit(1)
        
if __name__ == "__main__":
    main()    