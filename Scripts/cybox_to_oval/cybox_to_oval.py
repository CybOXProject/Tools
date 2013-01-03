#CybOX -> OVAL Translator
#v0.1 BETA
#Generates valid OVAL 5.7 XML output from CybOX v1.0 XML
#Supports Windows files, registry keys, and processes
import cybox_to_oval_processor as cybox2oval
import sys
    
#Print the usage text    
def usage():
    print USAGE_TEXT
    sys.exit(1)
    
USAGE_TEXT = """
CybOX --> OVAL XML Converter Utility
v0.1 BETA // Compatible with CybOX v1.0/OVAL 5.7

Usage: python cybox_to_oval.py <flags> -i <cybox xml file> -o <oval xml file>

Available Flags:
    -v: Verbose output mode. Lists any skipped observable items and also prints traceback for errors.
"""

def main():
    infilename = ''
    outfilename = ''
    global verbose_mode
    global skipped_observables
    verbose_mode = False
    skipped_observables = []
    #Get the command-line arguments
    args = sys.argv[1:]
    
    if len(args) < 4:
        usage()
        sys.exit(1)
        
    for i in range(0,len(args)):
        if args[i] == '-i':
            infilename = args[i+1]
        elif args[i] == '-o':
            outfilename = args[i+1]
        elif args[i] == '-v':
            verbose_mode = True

    processor = cybox2oval.cybox_to_oval_processor(infilename, outfilename, verbose_mode)
    #Parse the input CybOX and generate the output OVAL
    processor.generate_oval()
        
if __name__ == "__main__":
    main()    