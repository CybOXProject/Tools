#OpenIOC to CybOX Translator
#v0.1 BETA
#Generates valid CybOX v1.0 XML output from OpenIOCs
import openioc
import cybox.cybox_1_0 as cybox
import cybox.common_types_1_0 as common
import ioc_observable
import sys
import os
import traceback

#Normalize any ids used in the IOC to make the compatible with CybOX
#This is just in case the normal UUID type is not used
def normalize_id(id):
    if id.count(':') > 0:
        return id.replace(':','-')
    else:
        return id

#Test a value, if it is not an empty string or None, return it, otherwise return an empty string
def string_test(value):
    if value is not None and len(str(value)) > 0:
        return value
    else:
        return ''

#Build up a string representation of an entire OpenIOC IndicatorItem
def get_indicatoritem_string(indicatoritem, separator = None):
    context = indicatoritem.get_Context()
    content = indicatoritem.get_Content()
    condition = string_test(indicatoritem.get_condition())
    context_search = string_test(context.get_search())
    context_document = string_test(context.get_document())
    context_type = string_test(context.get_type())
    content_type = string_test(content.get_type())
    content_value = string_test(content.get_valueOf_())
    comment = string_test(indicatoritem.get_Comment())
    if separator is None:
        indicatoritem_string = condition + context_search + context_document\
        + context_type + content_type + content_value
    else:
        indicatoritem_string = condition + separator + context_search + separator\
        + context_document + separator + context_type + separator + content_type\
        + separator +  content_value
    return indicatoritem_string

#Map an IndicatorItem condition to a CybOX operator
def map_condition_keywords(condition):
    condition_dict = {
        'is':'Equals',
        'isnot':'DoesNotEqual',
        'contains':'Contains',
        'containsnot':'DoesNotContain'
    }
    return condition_dict.get(condition)

#Process an indicator item and create a single observable from it
def process_indicator_item(indicator_item, observables = None, indicatoritem_dict = None):
    context = indicator_item.get_Context()
    content = indicator_item.get_Content()
    search_string = context.get_search()
    content_string = content.get_valueOf_().rstrip()
    condition = indicator_item.get_condition()

    defined_object = ioc_observable.createObj(search_string, content_string, map_condition_keywords(condition))
    if defined_object != None:
        if observables != None:
            id_string = ''
            if indicator_item.get_id() is not None:
                id_string = 'openioc:indicator-item-' + normalize_id(indicator_item.get_id())
            else:
                id_string = 'openioc:indicator-item-' + generate_observable_id()
                indicatoritem_dict[get_indicatoritem_string(indicator_item)] = id_string
            observable = cybox.ObservableType(id=id_string)
            stateful_measure = cybox.StatefulMeasureType()
            cybox_object = cybox.ObjectType(id='cybox:object-' + generate_object_id())
            cybox_object.set_Defined_Object(defined_object)
            stateful_measure.set_Object(cybox_object)
            observable.set_Stateful_Measure(stateful_measure)
            observables.add_Observable(observable)
        return True
    else:
        if verbose_mode:
            skipped_indicatoritem = ''
            if indicator_item.get_id() is not None:
                skipped_indicatoritem = indicator_item.get_id()
            else:
                skipped_indicatoritem = get_indicatoritem_string(indicator_item, '_')
            if skipped_indicatoritem not in skipped_indicators:
                    skipped_indicators.append(skipped_indicatoritem)
        return False
    return

#Test if an indicator is 'compatible', that is if it has at least one indicator item that is compatible with CybOX
def test_compatible_indicator(indicator):
    for indicator_item in indicator.get_IndicatorItem():
        if process_indicator_item(indicator_item):
            return True
    #Recurse as needed to handle embedded indicators
    for embedded_indicator in indicator.get_Indicator():
        return test_compatible_indicator(embedded_indicator)
    
    return False

#Process a single indicator and create the associated observable structure
def process_indicator(indicator, observables, observable_composition, top_level=True):
    if test_compatible_indicator(indicator):
        #Dictionary for keeping track of indicatoritems without IDs
        indicatoritem_dict = {}
        current_composition = None
        if top_level == False:
            observable = cybox.ObservableType(id='openioc:indicator-' + normalize_id(indicator.get_id()))
            nested_observable_composition = cybox.ObservableCompositionType(operator=indicator.get_operator())
            observable.set_Observable_Composition(nested_observable_composition)
            observable_composition.add_Observable(observable)
            current_composition = nested_observable_composition
        elif top_level == True:
            current_composition = observable_composition
        
        for indicator_item in indicator.get_IndicatorItem():
            if process_indicator_item(indicator_item, observables, indicatoritem_dict):
                if indicator_item.get_id() is not None:
                    observable = cybox.ObservableType(idref='openioc:indicator-item-' + normalize_id(indicator_item.get_id()))
                else:
                    observable = cybox.ObservableType(idref=indicatoritem_dict.get(get_indicatoritem_string(indicator_item)))
                current_composition.add_Observable(observable)
                
        #Recurse as needed to handle embedded indicators
        for embedded_indicator in indicator.get_Indicator():
            process_indicator(embedded_indicator, observables, current_composition, False)
    return

#Generate CybOX output from the OpenIOC indicators
def generate_cybox(indicators):
    #Create the core CybOX structure
    observables = cybox.ObservablesType()
    #Set the description if it exists
    description = None
    if indicators.get_description() != None:
        description = indicators.get_description()
    elif indicators.get_short_description != None:
        description = indicators.get_short_description()
    
    indicator_definition = indicators.get_definition()
    for indicator in indicator_definition.get_Indicator():
        #Create the 'indicator' observable for holding the boolean indicator logic
        id_string = ''
        if indicator.get_id() is not None:
            id_string = 'openioc:indicator-' + normalize_id(indicator.get_id())
        else:
            id_string = 'openioc:indicator-' + generate_observable_id()
        indicator_observable = cybox.ObservableType(id=id_string)
        #Set the title as appropriate
        if description != None:
            indicator_observable.set_Title(description)
        composition = cybox.ObservableCompositionType(operator=indicator.get_operator())
        #Process the indicator, including any embedded indicators
        process_indicator(indicator, observables, composition, True)
        indicator_observable.set_Observable_Composition(composition)
        observables.add_Observable(indicator_observable)
    return observables 

#Helper methods
def generate_observable_id():
    global obsv_id_base
    obsv_id_base += 1
    return str(obsv_id_base)

def generate_object_id():
    global obj_id_base
    obj_id_base += 1
    return str(obj_id_base)
    
#Print the usage text    
def usage():
    print USAGE_TEXT
    sys.exit(1)
    
USAGE_TEXT = """
OpenIOC --> CybOX XML Converter Utility
v0.1 BETA // Compatible with CybOX v1.0

Usage: python openioc_to_cybox.py <flags> -i <openioc xml file> -o <cybox xml file>

Available Flags:
    -v: Verbose output mode. Lists any skipped indicator items and also prints traceback for errors.
"""
obsv_id_base = 0    
obj_id_base = 0

def main():
    infilename = ''
    outfilename = ''
    global verbose_mode
    global skipped_indicators
    verbose_mode = False
    skipped_indicators = []
    
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
            
    #Basic input file checking
    if os.path.isfile(infilename):    
        #Parse the OpenIOC file
        indicators = openioc.parse(infilename)
        try:
            print 'Generating ' + outfilename + ' from ' + infilename + '...'
            observables = generate_cybox(indicators)
            observables.set_cybox_major_version('1')
            observables.set_cybox_minor_version('0')
            observables.export(open(outfilename, 'w'), 0, namespacedef_='xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
 xmlns:openioc="http://schemas.mandiant.com/2010/ioc"\
 xmlns:cybox="http://cybox.mitre.org/cybox_v1"\
 xmlns:AccountObj="http://cybox.mitre.org/objects#AccountObject"\
 xmlns:AddressObj="http://cybox.mitre.org/objects#AddressObject"\
 xmlns:Common="http://cybox.mitre.org/Common_v1"\
 xmlns:DiskObj="http://cybox.mitre.org/objects#DiskObject"\
 xmlns:DiskPartitionObj="http://cybox.mitre.org/objects#DiskPartitionObject"\
 xmlns:DNSRecordObj="http://cybox.mitre.org/objects#DNSRecordObject"\
 xmlns:FileObj="http://cybox.mitre.org/objects#FileObject"\
 xmlns:MemoryObj="http://cybox.mitre.org/objects#MemoryObject"\
 xmlns:NetworkRouteEntryObj="http://cybox.mitre.org/objects#NetworkRouteEntryObject"\
 xmlns:PortObj="http://cybox.mitre.org/objects#PortObject"\
 xmlns:ProcessObj="http://cybox.mitre.org/objects#ProcessObject"\
 xmlns:SystemObj="http://cybox.mitre.org/objects#SystemObject"\
 xmlns:UnixFileObj="http://cybox.mitre.org/objects#UnixFileObject"\
 xmlns:UserAccountObj="http://cybox.mitre.org/objects#UserAccountObject"\
 xmlns:VolumeObj="http://cybox.mitre.org/objects#VolumeObject"\
 xmlns:WinDriverObj="http://cybox.mitre.org/objects#WinDriverObject"\
 xmlns:WinEventLogObj="http://cybox.mitre.org/objects#WinEventLogObject"\
 xmlns:WinExecutableFileObj="http://cybox.mitre.org/objects#WinExecutableFileObject"\
 xmlns:WinFileObj="http://cybox.mitre.org/objects#WinFileObject"\
 xmlns:WinHandleObj="http://cybox.mitre.org/objects#WinHandleObject"\
 xmlns:WinKernelHookObj="http://cybox.mitre.org/objects#WinKernelHookObject"\
 xmlns:WinProcessObj="http://cybox.mitre.org/objects#WinProcessObject"\
 xmlns:WinRegistryKeyObj="http://cybox.mitre.org/objects#WinRegistryKeyObject"\
 xmlns:WinServiceObj="http://cybox.mitre.org/objects#WinServiceObject"\
 xmlns:WinSystemObj="http://cybox.mitre.org/objects#WinSystemObject"\
 xmlns:WinUserAccountObj="http://cybox.mitre.org/objects#WinUserAccountObject"\
 xmlns:WinVolumeObj="http://cybox.mitre.org/objects#WinVolumeObject"\
 xsi:schemaLocation="http://cybox.mitre.org/Common_v1 http://cybox.mitre.org/XMLSchema/cybox_common_types_v1.0(draft).xsd\
 http://cybox.mitre.org/objects#AccountObject http://cybox.mitre.org/XMLSchema/objects/Account/Account_Object_1.1.xsd\
 http://cybox.mitre.org/objects#AddressObject http://cybox.mitre.org/XMLSchema/objects/Address/Address_Object_1.1.xsd\
 http://cybox.mitre.org/objects#DiskObject http://cybox.mitre.org/XMLSchema/objects/Disk/Disk_Object_1.2.xsd\
 http://cybox.mitre.org/objects#DiskPartitionObject http://cybox.mitre.org/XMLSchema/objects/Disk_Partition/Disk_Partition_Object_1.2.xsd\
 http://cybox.mitre.org/objects#DNSRecordObject http://cybox.mitre.org/XMLSchema/objects/DNS_Record/DNS_Record_Object_1.0.xsd\
 http://cybox.mitre.org/objects#FileObject http://cybox.mitre.org/XMLSchema/objects/File/File_Object_1.2.xsd\
 http://cybox.mitre.org/objects#MemoryObject http://cybox.mitre.org/XMLSchema/objects/Memory/Memory_Object_1.1.xsd\
 http://cybox.mitre.org/objects#NetworkRouteEntryObject http://cybox.mitre.org/XMLSchema/objects/Network_Route_Entry/Network_Route_Entry_Object_1.0.xsd\
 http://cybox.mitre.org/objects#PortObject http://cybox.mitre.org/XMLSchema/objects/Port/Port_Object_1.2.xsd\
 http://cybox.mitre.org/objects#ProcessObject http://cybox.mitre.org/XMLSchema/objects/Process/Process_Object_1.2.xsd\
 http://cybox.mitre.org/objects#SystemObject http://cybox.mitre.org/XMLSchema/objects/System/System_Object_1.2.xsd\
 http://cybox.mitre.org/objects#UnixFileObject http://cybox.mitre.org/XMLSchema/objects/Unix_File/Unix_File_Object_1.2.xsd\
 http://cybox.mitre.org/objects#UserAccountObject http://cybox.mitre.org/XMLSchema/objects/User_Account/User_Account_Object_1.1.xsd\
 http://cybox.mitre.org/objects#VolumeObject http://cybox.mitre.org/XMLSchema/objects/Volume/Volume_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinDriverObject http://cybox.mitre.org/XMLSchema/objects/Win_Driver/Win_Driver_Object_1.1.xsd\
 http://cybox.mitre.org/objects#WinEventLogObject http://cybox.mitre.org/XMLSchema/objects/Win_Event_Log/Win_Event_Log_Object_1.1.xsd\
 http://cybox.mitre.org/objects#WinExecutableFileObject http://cybox.mitre.org/XMLSchema/objects/Win_Executable_File/Win_Executable_File_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinFileObject http://cybox.mitre.org/XMLSchema/objects/Win_File/Win_File_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinHandleObject http://cybox.mitre.org/XMLSchema/objects/Win_Handle/Win_Handle_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinKernelHookObject http://cybox.mitre.org/XMLSchema/objects/Win_Kernel_Hook/Win_Kernel_Hook_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinProcessObject http://cybox.mitre.org/XMLSchema/objects/Win_Process/Win_Process_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinRegistryKeyObject http://cybox.mitre.org/XMLSchema/objects/Win_Registry_Key/Win_Registry_Key_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinServiceObject http://cybox.mitre.org/XMLSchema/objects/Win_Service/Win_Service_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinServiceObject http://cybox.mitre.org/XMLSchema/objects/Win_System/Win_System_Object_1.1.xsd\
 http://cybox.mitre.org/objects#WinUserAccountObject http://cybox.mitre.org/XMLSchema/objects/Win_User_Account/Win_User_Account_Object_1.2.xsd\
 http://cybox.mitre.org/objects#WinVolumeObject http://cybox.mitre.org/XMLSchema/objects/Win_Volume/Win_Volume_Object_1.2.xsd\
 http://cybox.mitre.org/cybox_v1 http://cybox.mitre.org/XMLSchema/cybox_core_v1.0(draft).xsd"')
            if verbose_mode:
                for indicator_id in skipped_indicators:
                    print "Indicator Item " + indicator_id + " Skipped; indicator type currently not supported"
            
        except Exception, err:
           print('\nError: %s\n' % str(err))
           if verbose_mode:
            traceback.print_exc()
           
    else:
        print('\nError: Input file not found or inaccessible.')
        sys.exit(1)
        
if __name__ == "__main__":
    main()    