#Snort to CybOX Translator
#v0.1 BETA
#Generates valid CybOX v1.0 XML output
#1 Snort rule = 1 CybOX observable

import snort_parser as parser
import sys
import os
import traceback
import cybox.cybox_1_0 as cybox
import cybox.common_types_1_0 as common
import cybox.network_packet_object_1_0 as netpacketobj
import cybox.address_object_1_1 as addressobj
import cybox.port_object_1_2 as portobj

#Extract the CybOX observable title from the Snort rule
def get_option(options, rule_name):
    for option in options:
        if option.strip(';') == rule_name:
            return option.strip(';')
        split_option = option.split(':')
        if split_option[0] == rule_name:
            return split_option[1].replace('"','').rstrip(';')
    return None

#Check a string to see if it is a snort variable or non-integer expression
def is_var(input_string):
    if input_string[0] == '$' or input_string == 'any':
        return True
    else:
        return False

#Normalize a Snort PCRE string to be generally PCRE compatible and add it to the CybOX datatype
def create_pcre_data_object(rule, pcre_expression):
    #First, normalize the expression
    split_pcre = pcre_expression.split(':')
    pcre_string = split_pcre[1].replace('"','').rstrip(';')
    split_pcre_string = pcre_string.split('/')
    normalized_modifiers = split_pcre_string[len(split_pcre_string)-1].strip('RUIPHDMCKSYBO')
    normalized_pcre_string = '/' + split_pcre_string[1] + '/' + normalized_modifiers
    cdata_pcre_string = '<![CDATA[' + normalized_pcre_string + ']]>'
    #Add it to the datatype
    datatype = common.DataSegmentType(Data_Format='Text')
    data_segment = common.StringObjectAttributeType(datatype='String', condition='FitsPattern', pattern_type='Regex', regex_syntax='PCRE', valueOf_=cdata_pcre_string)
    datatype.set_Data_Segment(data_segment)
    if get_option(rule.get('options'), 'dsize'):
        dsize = get_option(rule.get('options'), 'dsize')
        datatype.set_Data_Size(process_dsize(dsize))
    return datatype

#Process the Snort dsize rule
def process_dsize(dsize):
    if dsize.count('<>') == 1:
        split_dsize = dsize.split('<>')
        data_size = common.DataSizeType(datatype='String', condition='IsInRange', units='Bytes', start_range=split_dsize[0], end_range=split_dsize[1])
        return data_size
    else:
        data_size = common.DataSizeType(datatype='String', units='Bytes', valueOf_=dsize)
        return set_rule_conditions(data_size)
    
#Create a CybOX datatype object for the content
def create_content_data_object(rule, content):
    datatype = common.DataSegmentType()
    content_string = get_option(content, 'content')
    condition = 'Contains'
    dataformat = 'Text'
    if content_string[0] == '!':
        condition = 'DoesNotContain'
        content_string = content_string.strip('!')
    if content_string.count('|') > 0:
        content_string = content_string.strip('|')
        dataformat = 'Binary'
    if get_option(content, 'offset'):
        datatype.set_Offset(common.IntegerObjectAttributeType(datatype='Int',valueOf_=get_option(content, 'offset')))
    if get_option(content, 'distance'):
        datatype.set_Search_Distance(common.IntegerObjectAttributeType(datatype='Int',valueOf_=get_option(content, 'distance')))
    if get_option(content, 'within'):
        datatype.set_Search_Within(common.IntegerObjectAttributeType(datatype='Int',valueOf_=get_option(content, 'within')))
    cdata_content_string = '<![CDATA[' + content_string + ']]>'
    datatype.set_Data_Format(dataformat)
    datatype.set_Data_Segment(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=cdata_content_string))
    if get_option(rule.get('options'), 'dsize'):
        dsize = get_option(rule.get('options'), 'dsize')
        datatype.set_Data_Size(process_dsize(dsize))
    return datatype

#Set the appropriate condition based on the rule data
def set_rule_conditions(ruledata):
    rulevalue = ruledata.get_valueOf_()
    if rulevalue.count('!') == 0 and rulevalue.count('>') == 0 and rulevalue.count('<') == 0:
        if rulevalue.count('-') == 1:
            split_value = rulevalue.split('-')
            ruledata.set_valueOf_('')
            ruledata.set_condition('IsInRange')
            if split_value[0] == '':
                ruledata.set_start_range('0')
                ruledata.set_end_range(split_value[1])
            elif split_value[1] == '':
                ruledata.set_start_range(split_value[0])
                ruledata.set_end_range('255')
            else:
                ruledata.set_start_range(split_value[0])
                ruledata.set_end_range(split_value[1])
        else:
            ruledata.set_condition('Equals')
    elif rulevalue.count('!') == 1:
        ruledata.set_valueOf_(rulevalue.strip('!'))
        ruledata.set_condition('DoesNotEqual')
    elif rulevalue.count('>') == 1:
        if rulevalue.count('>=') == 1:
            ruledata.set_valueOf_(rulevalue.strip('>='))
            ruledata.set_condition('GreaterThanOrEqual')
        else:
            ruledata.set_valueOf_(rulevalue.strip('>'))
            ruledata.set_condition('GreaterThan')
    elif rulevalue.count('<') == 1:
        if rulevalue.count('<=') == 1:
            ruledata.set_valueOf_(rulevalue.strip('<='))
            ruledata.set_condition('LessThanOrEqual')
        else:
            ruledata.set_valueOf_(rulevalue.strip('<'))
            ruledata.set_condition('LessThan')
    return ruledata

#Set any IP options
def set_ip_options(ipopts):
    ipv4_options = netpacketobj.IPv4OptionType()
    ipopts_dict = {'rr':'recordroute(7)',
                   'eol':'endofoptionslist(0)',
                   'nop':'nop(1)',
                   'ts':'timestamp(4)',
                   'sec':'security(2)',
                   'esec':'extendedsecurity(5)',
                   'lsrr':'loosesourceroute(3)',
                   'lsrre':'loosesourceroute(3)',
                   'ssrr':'strictsourceroute(9)',
                   'satid':'streamidentifier(8)'}
    if ipopts == 'any':
        ipv4_options.set_Option(common.StringObjectAttributeType(datatype='String', condition='FitsPattern', pattern_type='Regex', regex_syntax='PCRE', valueOf_='.*'))
    else:
        ipv4_options.set_Option(common.StringObjectAttributeType(datatype='String', condition='Equals', valueOf_=ipopts_dict.get(ipopts)))
    return ipv4_options

#Set the fragmentation bits options
def set_fragbits(fragbits):
    ipv4_flags = netpacketobj.IPv4FlagsType()
    condition = 'Equals'
    if fragbits.count('!') == 1:
        condition = 'DoesNotEqual'
    if fragbits.count('M') == 1:
        more_fragments = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_='morefragmentstofollow(1)')
        ipv4_flags.set_More_Fragments(more_fragments)
    if fragbits.count('R') == 1:
        ipv4_flags.set_reserved('True')
    if fragbits.count('D') == 1:
        do_not_fragment = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_='donotfragment(1)')
        ipv4_flags.set_Do_Not_Fragment(do_not_fragment)
    return ipv4_flags
        
#Process any Snort IP rules
def process_ip_rules(rule, ipv4_header):
    #Handle the fragment offset option
    if get_option(rule.get('options'), 'fragoffset'):
        fragoffset = set_rule_conditions(common.PositiveIntegerObjectAttributeType(valueOf_=get_option(rule.get('options'), 'fragoffset')))
        ipv4_header.set_Fragment_Offset(fragoffset)
    if get_option(rule.get('options'), 'ttl'):
        ttl = set_rule_conditions(common.PositiveIntegerObjectAttributeType(valueOf_=get_option(rule.get('options'), 'ttl')))
        ipv4_header.set_TTL(ttl)
    if get_option(rule.get('options'), 'id'):
        ipid = set_rule_conditions(common.PositiveIntegerObjectAttributeType(valueOf_=get_option(rule.get('options'), 'id')))
        ipv4_header.set_Identification(ipid)
    if get_option(rule.get('options'), 'fragbits'):
        fragbits = set_fragbits(get_option(rule.get('options'), 'fragbits'))
        ipv4_header.set_Flags(fragbits)

#Process any Snort TCP rules
def process_tcp_rules(rule, tcp_header):
    if get_option(rule.get('options'), 'seq'):
        seq = set_rule_conditions(common.PositiveIntegerObjectAttributeType(valueOf_=get_option(rule.get('options'), 'seq')))
        tcp_header.set_SeqNum(seq)
    if get_option(rule.get('options'), 'ack'):
        ack = set_rule_conditions(common.PositiveIntegerObjectAttributeType(valueOf_=get_option(rule.get('options'), 'ack')))
        tcp_header.set_ACKNum(ack)
    if get_option(rule.get('options'), 'window'):
        window = set_rule_conditions(common.PositiveIntegerObjectAttributeType(valueOf_=get_option(rule.get('options'), 'window')))
        tcp_header.set_Window(window)

#Process the IP header addresses
def process_ip_header_address(rule, ipv4_header):
    src_ip = rule.get('src_ip')
    dst_ip = rule.get('dst_ip')
    if not is_var(dst_ip) or not is_var(src_ip):
        ipv4_header.set_IP_Version(common.StringObjectAttributeType(datatype='String', valueOf_='IPv4(4)'))
        if not is_var(dst_ip):
            if dst_ip.count(',') == 0:
                address_value = addressobj.Address_Value(datatype='String', condition='Equals', valueOf_=dst_ip)
            elif dst_ip.count(',') >= 1:
                address_value = addressobj.Address_Value(datatype='String', condition='IsInSet', ValueSet=dst_ip)
            ip_address = addressobj.AddressObjectType(category='ipv4-addr', Address_Value=address_value)
            ipv4_header.set_Dest_IPv4_Addr(ip_address)
        if not is_var(src_ip):
            if src_ip.count(',') == 0:
                address_value = addressobj.Address_Value(datatype='String', condition='Equals', valueOf_=src_ip)
            elif src_ip.count(',') >= 1:
                address_value = addressobj.Address_Value(datatype='String', condition='IsInSet', ValueSet=src_ip)
            ip_address = addressobj.AddressObjectType(category='ipv4-addr', Address_Value=address_value)
            ipv4_header.set_Src_IPv4_Addr(ip_address)

#Create the IP layer w/ ip/port data
def create_ip_layer(rule):
    ip_layer = netpacketobj.InternetLayerType()
    ipv4_packet = netpacketobj.IPv4PacketType()
    ipv4_header = netpacketobj.IPv4HeaderType()
    process_ip_header_address(rule, ipv4_header)
    process_ip_rules(rule, ipv4_header)
    if get_option(rule.get('options'), 'ipopts'):
        ipopts = set_ip_options(get_option(rule.get('options'), 'ipopts'))
        if ipopts.hasContent_():
            ipv4_packet.add_Option(ipopts)
    ipv4_packet.set_IPv4_Header(ipv4_header)
    ip_layer.set_IPv4(ipv4_packet)
    if ipv4_header.hasContent_():
        return ip_layer
    else:
        return None

#Create a Port Object based on the Snort port (which allows ranges)
def create_port(port):
    comma_count = port.count(',')
    if comma_count == 0:
        split_port = port.split(':')
        if len(split_port) == 1:
            port_value = portobj.Port_Value(datatype='PositiveInteger', condition='Equals', valueOf_=port)
        elif len(split_port) == 2:
            if split_port[0] == '':
                port_value = portobj.Port_Value(datatype='PositiveInteger', condition='IsInRange', end_range=split_port[1])
            elif split_port[1] == '':
                 port_value = portobj.Port_Value(datatype='PositiveInteger', condition='IsInRange', start_range=split_port[0])
            else:
                port_value = portobj.Port_Value(datatype='PositiveInteger', condition='IsInRange', start_range=split_port[0], end_range=split_port[1])
    elif comma_count >= 1:
        if port.count(':') == 0:
            port_value = portobj.Port_Value(datatype='PositiveInteger', condition='IsInSet', value_set=port)
                
    port = portobj.PortObjectType(Port_Value=port_value)       
    return port

#Create the transport layer w/ TCP data       
def create_transport_layer(rule, protocol, content, content_type):
    transport_layer = None
    dst_port = rule.get('dst_port')
    src_port = rule.get('src_port')
    if content != None:
        transport_layer = netpacketobj.TransportLayerType()
        if content_type == 'pcre':
            data = create_pcre_data_object(rule, content)
        elif content_type == 'content':
            data = create_content_data_object(rule, content)
        if protocol == 'tcp':
            tcp_object = netpacketobj.TCPType(Data=data)
            tcp_header = netpacketobj.TCPHeaderType()
            process_tcp_rules(rule, tcp_header)
            if not is_var(src_port) or not is_var(dst_port):
                if not is_var(src_port):
                    tcp_header.set_Src_Port(create_port(src_port))
                if not is_var(dst_port):
                    tcp_header.set_Dest_Port(create_port(dst_port))
            if tcp_header.hasContent_():
                tcp_object.set_TCP_Header(tcp_header)
            transport_layer.set_TCP(tcp_object)
        elif protocol == 'udp':
            udp_object = netpacketobj.UDPType(Data=data)
            if not is_var(src_port) or not is_var(dst_port):
                udp_header = netpacketobj.UDPHeaderType()
                if not is_var(src_port):
                    udp_header.set_SrcPort(create_port(src_port))
                if not is_var(dst_port):
                    udp_header.set_DestPort(create_port(dst_port))
                udp_object.set_UDP_Header(udp_header)
            transport_layer.set_UDP(udp_object)
    return transport_layer

#Create an observable component that goes into the observable_composition element
def create_observable_component(rule, protocol, content, content_type):
    observable_component = cybox.ObservableType()
    #Create the stateful measure
    stateful_measure = cybox.StatefulMeasureType()
    id_string = 'cybox:object-' + generate_object_id()
    cybox_object = cybox.ObjectType()
    cybox_object.set_id(id_string)
    packet_object = netpacketobj.NetworkPacketType()
    packet_object.set_object_reference(None)
    transport_layer = create_transport_layer(rule, protocol, content, content_type)
    ip_layer = create_ip_layer(rule)
    if transport_layer != None:
        packet_object.set_Transport_Layer(transport_layer)
    if ip_layer != None:
        packet_object.set_Internet_Layer(ip_layer)
    packet_object.set_anyAttributes_({'xsi:type' : 'PacketObj:NetworkPacketType'})
    #Set the CybOX objects and stateful measure
    cybox_object.set_Defined_Object(packet_object)
    stateful_measure.set_Object(cybox_object)
    observable_component.set_Stateful_Measure(stateful_measure)
    return observable_component

#Check if the port is list with ranges
#This is a special case that requires separate logic
def check_port_range_list(port):
    if not is_var(port) and port.count(',') >= 1:
        if port.count(':') >=1:
            ranges = []
            values = ''
            split_port = port.split(',')
            for port_value in split_port:
                if port_value.count(':') == 1:
                    ranges.append(port_value)
                elif port_value.count(':') == 0:
                    values += (port_value + ',')
            values = values.rstrip(',')
            return [ranges,values]
    return None

#Create an observable or observable composition from a rule based on its 'content' or 'pcre' entries
def create_observable_composition(rule, protocol, composition = False):
    component_count = 0
    embedded_observable = cybox.ObservableType()
    embedded_observable_composition = cybox.ObservableCompositionType(operator='AND')
    if rule.get('content_statement') != None:
        #Loop through and add the observable components
        for content in rule.get('content_statement'):
            observable_component = create_observable_component(rule, protocol, content, 'content')
            if observable_component != None:
                embedded_observable_composition.add_Observable(observable_component)
                component_count += 1
    if rule.get('pcre_statement') != None:
        for pcre in rule.get('pcre_statement'):
            observable_component = create_observable_component(rule, protocol, pcre, 'pcre')
            if observable_component != None:
                embedded_observable_composition.add_Observable(observable_component)
                component_count += 1
    #Finally, set the composition in the top-level observable
    if component_count > 0:
        embedded_observable.set_Observable_Composition(embedded_observable_composition)
        if composition == True:
            return embedded_observable_composition
        else:
            return embedded_observable
    else:
        return None

#Special function for creating observables based on port lists with ranges
def create_port_based_observable(rule, protocol, port_type, ports, single_mode=True):
    observables = []
    if port_type == 'dst_port':
        other_port = 'src_port'
        old_port = rule.get('src_port')
    elif port_type == 'src_port':
        other_port = 'dst_port'
        old_port = rule.get('dst_port')
    ranges = ports[0]
    values = ports[1]
    embedded_observable = cybox.ObservableType()
    embedded_observable_composition = cybox.ObservableCompositionType(operator='OR')
    rule[other_port] = '$variable'
    for port_range in ranges:
        rule[port_type] = port_range
        embedded_observable_composition.add_Observable(create_observable_composition(rule, protocol))
    rule[port_type] = values
    embedded_observable_composition.add_Observable(create_observable_composition(rule, protocol))
    embedded_observable.set_Observable_Composition(embedded_observable_composition)
    if single_mode:
        rule[port_type] = '$variable'
        rule[other_port] = old_port
        observables.append(create_observable_composition(rule, protocol))
    
    observables.append(embedded_observable)
    
    return observables

#Create a single CybOX observable from a single Snort rule
def create_observable(rule):
    protocol = rule.get('protocol')
    #Currently we support only TCP and UDP rules
    if protocol == 'udp' or protocol == 'tcp':
        pass
    else:
        return None
    
    observable_id = None
    title = None
    options = rule.get('options')
    #Create the title
    if options != None:
        title = get_option(options, 'msg')
        observable_id = get_option(options, 'sid')
    
    #Create the observable
    
    observable = cybox.ObservableType()
    
    #Create the observable composition
    observable_composition = cybox.ObservableCompositionType(operator='AND')
    id_string = ''
    if observable_id != None:
        id_string = 'cybox:observable-' + observable_id
    else:
        id_string = 'cybox:observable-' + generate_observable_id()
    observable.set_id(id_string)
    
    if title != None:
        observable.set_Title(title)
    
    #Check if the ports are a range list or not        
    src_ports = check_port_range_list(rule.get('src_port'))
    dst_ports = check_port_range_list(rule.get('dst_port'))
    
    if src_ports != None and dst_ports == None:
        observable_list = create_port_based_observable(rule, protocol, 'src_port', src_ports)
        for obsv in observable_list:
            observable_composition.add_Observable(obsv)
    elif src_ports == None and dst_ports != None:
        observable_list = create_port_based_observable(rule, protocol, 'dst_port', dst_ports)
        for obsv in observable_list:
            observable_composition.add_Observable(obsv)
    elif src_ports != None and dst_ports != None:
        observable_list = create_port_based_observable(rule, protocol, 'src_port', src_ports, False)
        for obsv in observable_list:
            observable_composition.add_Observable(obsv)
        observable_list = create_port_based_observable(rule, protocol, 'dst_port', dst_ports, False)
        for obsv in observable_list:
            observable_composition.add_Observable(obsv)
    elif src_ports == None and dst_ports == None:
        observable_composition = create_observable_composition(rule, protocol, True)
    if observable_composition.hasContent_():
        observable.set_Observable_Composition(observable_composition)
        return observable
    else:
        return None
     
#Generate the CybOX observables from the Snort rules
def generate_cybox(parsed_rules):
    global processed_rules
    global skipped_rules
    #Create the core CybOX structure
    observables = cybox.ObservablesType()
    for rule in parsed_rules:
        observable = create_observable(rule)
        if observable != None:
            observables.add_Observable(observable)
            processed_rules += 1
        else:
            skipped_rules += 1
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
Snort Rule --> CybOX XML Converter Utility
v0.1 BETA // Compatible with CybOX v1.0

Usage: python snort_to_cybox.py <optional flags> -i <snort rule file> -o <cybox xml file>
Optional Flags:
    -v: Verbose error output
"""
obsv_id_base = 0    
obj_id_base = 0
processed_rules = 0
skipped_rules = 0

def main():
    global skipped_rules
    global processed_rules
    infilename = ''
    outfilename = ''
    print_stats = False
    
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
        elif args[i] == '-s':
            print_stats = True
    #Basic input file checking
    if os.path.isfile(infilename):    
        #Create the main parser object
        snort_parser = parser.snort_parser()
        try:
            print 'Generating ' + outfilename + ' from ' + infilename + '...'
            parsed_rules = snort_parser.parse_rule_file(infilename)
            observables = generate_cybox(parsed_rules)
            observables.set_cybox_major_version('1')
            observables.set_cybox_minor_version('0')
            observables.export(open(outfilename, 'w'), 0, namespacedef_='xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
 xmlns:Common="http://cybox.mitre.org/Common_v1"\
 xmlns:cybox="http://cybox.mitre.org/cybox_v1"\
 xmlns:PacketObj="http://cybox.mitre.org/objects#PacketObject"\
 xmlns:AddressObj="http://cybox.mitre.org/objects#AddressObject"\
 xmlns:PortObj="http://cybox.mitre.org/objects#PortObject"\
 xsi:schemaLocation="http://cybox.mitre.org/Common_v1 http://cybox.mitre.org/XMLSchema/cybox_common_types_v1.0(draft).xsd\
 http://cybox.mitre.org/XMLSchema/objects#PacketObject http://cybox.mitre.org/XMLSchema/objects/Network_Packet/Network_Packet_Object_1.0.xsd\
 http://cybox.mitre.org/cybox_v1 http://cybox.mitre.org/XMLSchema/cybox_core_v1.0(draft).xsd"')
            
            if print_stats:
                skipped_rules = snort_parser.get_skipped_rules() + skipped_rules
                print ('\nRules Processed: ' + str(processed_rules))
                print ('Rules Skipped: ' + str(skipped_rules))
        except Exception, err:
           print('\nError: %s\n' % str(err))
           traceback.print_exc()
           
    else:
        print('\nError: Input file not found or inaccessible.')
        sys.exit(1)
        
if __name__ == "__main__":
    main()    
