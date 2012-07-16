#OpenIOC -> CybOX Translator
#v0.1 BETA
#Creates CybOX objects from IOC indicator item components 
import cybox.common_types_1_0 as common
import cybox.file_object_1_2 as fileobj
import cybox.win_file_object_1_2 as winfileobj
import cybox.unix_file_object_1_2 as unixfileobj
import cybox.win_executable_file_object_1_2 as winexecfileobj
import cybox.win_driver_object_1_1 as windriverobj
import cybox.win_kernel_hook_object_1_2 as hookobj
import cybox.port_object_1_2 as portobj
import cybox.address_object_1_1 as addressobj
import cybox.win_registry_key_object_1_2 as winregobj
import cybox.process_object_1_2 as processobj
import cybox.win_process_object_1_2 as winprocessobj
import cybox.win_event_log_object_1_1 as wineventlogobj
import cybox.account_object_1_1 as accountobj
import cybox.user_account_object_1_1 as useraccountobj
import cybox.win_user_account_object_1_2 as winuseraccountobj
import cybox.win_service_object_1_2 as winserviceobj
import cybox.volume_object_1_2 as volumeobj
import cybox.win_volume_object_1_2 as winvolumeobj
import cybox.disk_object_1_2 as diskobj
import cybox.dns_record_object_1_0 as dnsrecordobj
import cybox.uri_object_1_1 as uriobj
import cybox.network_route_entry_object_1_0 as netrouteentryobj
import cybox.win_system_object_1_1 as winsystemobj
import cybox.system_object_1_2 as systemobj
import cybox.win_handle_object_1_2 as winhandleobj
import cybox.memory_object_1_1 as memoryobj
import cybox.disk_partition_object_1_2 as diskpartitionobj

def createObj(search_string, content_string, condition):
    defined_object = None
    split_search_string = search_string.split('/',1)
    if split_search_string[0] == 'SystemInfoItem':
        defined_object = createSystemObj(search_string, content_string, condition)
    elif split_search_string[0] == 'RouteEntryItem':
        defined_object = createNetRouteObj(search_string, content_string, condition)
    elif split_search_string[0] == 'DnsEntryItem':
        defined_object = createDNSObj(search_string, content_string, condition)
    elif split_search_string[0] == 'DiskItem':
        defined_object = createDiskObj(search_string, content_string, condition)
    elif split_search_string[0] == 'VolumeItem':
        defined_object = createVolumeObj(search_string, content_string, condition)
    elif split_search_string[0] == 'ServiceItem':
        defined_object = createServiceObj(search_string, content_string, condition)
    elif split_search_string[0] == 'FileItem':
        defined_object = createFileObj(search_string, content_string, condition)
    elif split_search_string[0] == 'HookItem':
        defined_object = createHookObj(search_string, content_string, condition)
    elif split_search_string[0] == 'DriverItem':
        defined_object = createDriverObj(search_string, content_string, condition)
    elif split_search_string[0] == 'RegistryItem':
        defined_object = createRegObj(search_string, content_string, condition)
    elif split_search_string[0] == 'UserItem':
        defined_object = createUserObj(search_string, content_string, condition)
    elif split_search_string[0] == 'EventLogItem':
        defined_object = createWinEventLogObj(search_string, content_string, condition)
    elif split_search_string[0] == 'ProcessItem':
        defined_object = createProcessObj(search_string, content_string, condition)
    elif split_search_string[0] == 'PortItem':
        defined_object = createPortObj(search_string, content_string, condition)
    
    if defined_object != None: 
        if defined_object.hasContent_():
            defined_object.set_object_reference(None)
            return defined_object
    else:
        return None

def createWinSystemObj(search_string, content_string, condition):
    #Create the Windows system object
    winsysobj = winsystemobj.WindowsSystemObjectType()
    if search_string == 'SystemInfoItem/domain':
        stringobjattribute = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string))
        winsysobj.set_Domain(stringobjattribute)
    elif search_string == 'SystemInfoItem/productID':
        stringobjattribute = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string))
        winsysobj.set_Product_ID(stringobjattribute)
    elif search_string == 'SystemInfoItem/productName':
        stringobjattribute = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string))
        winsysobj.set_Product_Name(stringobjattrbute)
    elif search_string == 'SystemInfoItem/regOrg':
        stringobjattribute = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string))
        winsysobj.set_Registered_Organization(stringobjattrbute)
    elif search_string == 'SystemInfoItem/regOwner':
        stringobjattribute = common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string))
        winsysobj.set_Registered_Owner(stringobjattrbute)
    winsysobj.set_anyAttributes_({'xsi:type' : 'WinSystemObj:WindowsSystemObjectType'})

    return winsysobj
    
def createSystemObj(search_string, content_string, condition):
    #Create the system object
    sysobj = systemobj.SystemObjectType()
    if content_string == 'SystemInfoItem/MAC' or content_string == 'SystemInfoItem/networkArray/networkInfo/MAC':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        network_interface.set_MAC(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/OS': #Todo - find how IOC represents this
        pass
    elif content_string == 'SystemInfoItem/availphysical':
        sysobj.set_Available_Physical_Memory(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif content_string == 'SystemInfoItem/biosInfo/biosDate':
        bios_info = systemobj.BIOSInfoType()
        bios_info.set_BIOS_Date(common.DateObjectAttributeType(datatype='Date', condition=condition, valueOf_=content_string))
        sysobj.set_BIOS_Info(bios_info)
    elif content_string == 'SystemInfoItem/biosInfo/biosVersion':
        bios_info = systemobj.BIOSInfoType()
        bios_info.set_BIOS_Version(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        sysobj.set_BIOS_Info(bios_info)
    elif content_string == 'SystemInfoItem/buildNumber':
        os = systemobj.OS_Type()
        os.set_Build_Number(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        sysobj.set_OS(os)
    elif content_string == 'SystemInfoItem/date':
        sysobj.set_Date(common.DateObjectAttributeType(datatype='Date', condition=condition, valueOf_=content_string))
    elif content_string == 'SystemInfoItem/directory': #Todo - find what this means
        pass
    elif content_string == 'SystemInfoItem/domain':
        createWinSystemObj(search_string, content_string, condition)
    elif content_string == 'SystemInfoItem/hostname':
        sysobj.set_Hostname(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif content_string == 'SystemInfoItem/installDate':
        os = systemobj.OS_Type()
        os.set_Install_Date(common.DateObjectAttributeType(datatype='Date', condition=condition, valueOf_=content_string))
        sysobj.set_OS(os)
    elif content_string == 'SystemInfoItem/machine': #Todo - find what this means
        pass
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/adapter':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        network_interface.set_Adapter(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/description':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        network_interface.set_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/dhcpLeaseExpires':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        network_interface.set_DHCP_Lease_Expires(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/dhcpLeaseObtained':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        network_interface.set_DHCP_Lease_Obtained(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/dhcpServerArray/dhcpServer':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        dhcp_server_list = systemobj.DHCPServerListType()
        dhcp_server_address = addressobj.AddressObjectType(category='ipv4-addr')
        dhcp_server_address.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        dhcsp_server_list.add_DHCP_Server_Address(dhcp_server_address)
        network_interface.set_DHCP_Server_List(dhcp_server_list)
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif search_string == 'SystemInfoItem/networkArray/networkInfo/ipArray/ipInfo/ipAddress':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        ip_list = systemobj.IPInfoListType()
        ip_info = systemobj.IPInfoType()
        ip_address = addressobj.AddressObjectType(category='ipv4-addr')
        ip_address.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        ip_info.set_IP_Address(ip_address)
        ip_list.add_IP_Info(ip_info)
        network_interface.set_IP_List(ip_list)
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/ipArray/ipInfo/subnetMask':
        network_interface_list = systemobj.NetworkInterfaceListType()
        network_interface = systemobj.NetworkInterfaceType()
        ip_list = systemobj.IPInfoListType()
        ip_info = systemobj.IPInfoType()
        subnet_mask = addressobj.AddressObjectType(category='ipv4-addr')
        subnet_mask.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        ip_info.set_Subnet_Mask(subnet_mask)
        ip_list.add_IP_Info(ip_info)
        network_interface.set_IP_List(ip_list)
        network_interface_list.add_Network_Interface(network_interface)
        sysobj.set_Network_Interface_List(network_interface_list)
    elif content_string == 'SystemInfoItem/networkArray/networkInfo/ipGatewayArray/ipGateway': #Todo - define this in CybOX?
        pass
    elif content_string == 'SystemInfoItem/patchLevel':
        os = systemobj.OS_Type()
        os.set_Patch_Level(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        sysobj.set_OS(os)
    elif content_string == 'SystemInfoItem/procType': #Todo - find how IOC represents this
        sysobj.set_Processor_Architecture(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif content_string == 'SystemInfoItem/processor':
        sysobj.set_Processor(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif content_string == 'SystemInfoItem/productID':
        return createWinSystemObject(search_string, content_string, condition)
    elif content_string == 'SystemInfoItem/productName':
        return createWinSystemObject(search_string, content_string, condition)
    elif content_string == 'SystemInfoItem/regOrg':
        return createWinSystemObject(search_string, content_string, condition)
    elif content_string == 'SystemInfoItem/regOwner':
        return createWinSystemObject(search_string, content_string, condition)
    elif content_string == 'SystemInfoItem/timezoneDST':
        sysobj.set_Timezone_DST(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif content_string == 'SystemInfoItem/timezoneStandard':
        sysobj.set_Timezone_Standard(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif content_string == 'SystemInfoItem/totalphysical':
        sysobj.set_Total_Physical_Memory(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    sysobj.set_anyAttributes_({'xsi:type' : 'SystemObj:SystemObjectType'})

    return sysobj
    
def createNetRouteObj(search_string, content_string, condition):  
    #Create the network route entry object
    netrtobj = netrouteentryobj.NetworkRouteEntryObjectType()
    if search_string == "RouteEntryItem/Interface":
        netrtobj.set_Interface(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "RouteEntryItem/Destination":
        destination_address = addressobj.AddressObjectType(category='ipv4-addr')
        destination_address.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netrtobj.set_Destination_Address(destination_address)
    elif search_string == "RouteEntryItem/Gateway":
        gateway_address = addressobj.AddressObjectType(category='ipv4-addr')
        gateway_address.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netrtobj.set_Gateway_Address(gateway_address)
    elif search_string == "RouteEntryItem/Netmask":
        netmask = addressobj.AddressObjectType(category='ipv4-addr')
        netmask.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netrtobj.set_Netmask(netmask)
    elif search_string == "RouteEntryItem/RouteType": #Todo - find how IOC represents this
        netrtobj.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "RouteEntryItem/Protocol":
        netrtobj.set_Protocol(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "RouteEntryItem/Metric":
        netrtobj.set_Metric(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string == "RouteEntryItem/ValidLifetime": #Todo - find how IOC represents this
        netrtobj.set_Valid_Lifetime(common.DurationObjectAttributeType(datatype='Duration', condition=condition, valueOf_=content_string))
    elif search_string == "RouteEntryItem/PreferredLifetime": #Todo - find how IOC represents this
        netrtobj.set_Preferred_Lifetime(common.DurationObjectAttributeType(datatype='Duration', condition=condition, valueOf_=content_string))
    elif search_string == "RouteEntryItem/RouteAge": #Todo - find how IOC represents this
        netrtobj.set_Route_Age(common.DurationObjectAttributeType(datatype='Duration', condition=condition, valueOf_=content_string))
    elif search_string == "RouteEntryItem/IsLoopback":
        netrtobj.set_is_loopback(content_string)
    elif search_string == "RouteEntryItem/IsAutoconfigureAddress":
        netrtobj.set_is_autoconfigure_address(content_string)
    elif search_string == "RouteEntryItem/IsPublish":
        netrtobj.set_is_publish(content_string)
    elif search_string == "RouteEntryItem/IsImmortal":
        netrtobj.set_is_immortal(content_string)
    elif search_string == "RouteEntryItem/IsIPv6":
        netrtobj.set_is_ipv6(content_string)
    elif search_string == "RouteEntryItem/Origin":
        origin = addressobj.AddressObjectType(category='ipv4-addr')
        origin.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netrtobj.set_Origin(origin)

    netrtobj.set_anyAttributes_({'xsi:type' : 'NetworkRouteEntryObj:NetworkRouteEntryObjectType'})
    
    return netrtobj
    
def createDNSObj(search_string, content_string, condition):
    #Create the dns cache object
    dnsobj = dnsrecordobj.DNSRecordObjectType()
    if search_string == "DnsEntryItem/Host":
        uri = uriobj.URIObjectType()
        uri.set_Value(common.AnyURIObjectAttributeType(datatype='AnyURI', condition=condition, valueOf_=content_string))
        dnsobj.set_Domain_Name(uri)
    elif search_string == "DnsEntryItem/RecordName":
        dnsobj.set_Record_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "DnsEntryItem/RecordType":
        dnsobj.set_Record_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "DnsEntryItem/TimeToLive":
        dnsobj.set_TTL(process_numerical_value(common.IntegerObjectAttributeType(datatype='Int'), content_string, condition))
    elif search_string == "DnsEntryItem/Flags":
        dnsobj.set_Flags(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
    elif search_string == "DnsEntryItem/DataLength":
        dnsobj.set_Data_Length(process_numerical_value(common.IntegerObjectAttributeType(datatype='Int'), content_string, condition))
    elif search_string == "RecordData": #ToDo - determine how to represent this
        pass
    dnsobj.set_anyAttributes_({'xsi:type' : 'DNSCacheObj:DNSCacheObjectType'})

    return dnsobj
    
def createDiskObj(search_string, content_string, condition):
    #Create the disk object
    dskobj = diskobj.DiskObjectType()
    if search_string == "DiskItem/DiskName":
        dskobj.set_Disk_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "DiskItem/DiskSize":
        dskobj.set_Disk_Size(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string == "DiskItem/PartitionList/Partition/PartitionLength":
        partition_list = diskobj.PartitionListType()
        partition = diskpartitionobj.DiskPartitionObjectType()
        partition.set_Partition_Length(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        partition_list.add_Partition(partition)
        dskobj.set_Partition_List(partition_list)
    elif search_string == "DiskItem/PartitionList/Partition/PartitionNumber":
        partition_list = diskobj.PartitionListType()
        partition = diskpartitionobj.DiskPartitionObjectType()
        partition.set_Partition_ID(process_numerical_value(common.IntegerObjectAttributeType(datatype='Int'), content_string, condition))
        partition_list.add_Partition(partition)
        dskobj.set_Partition_List(partition_list)
    elif search_string == "DiskItem/PartitionList/Partition/PartitionOffset":
        partition_list = diskobj.PartitionListType()
        partition = diskpartitionobj.DiskPartitionObjectType()
        partition.set_Partition_Offset(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        partition_list.add_Partition(partition)
        dskobj.set_Partition_List(partition_list)
    elif search_string == "DiskItem/PartitionList/Partition/PartitionType": #Todo - find how IOC represents this
        partition_list = diskobj.PartitionListType()
        partition = diskpartitionobj.DiskPartitionObjectType()
        partition.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        partition_list.add_Partition(partition)
        dskobj.set_Partition_List(partition_list)
    dskobj.set_anyAttributes_({'xsi:type' : 'DiskObj:DiskObjectType'})
    
    return dskobj
 
def createWinVolumeObj(search_string, content_string, condition):
    #Create the volume object
    winvolobj = winvolumeobj.WindowsVolumeObjectType()
    if search_string == "VolumeItem/DriveLetter":
        winvolobj.set_Drive_Letter(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    winvolobj.set_anyAttributes_({'xsi:type' : 'WinVolumeObj:WindowsVolumeObjectType'})

    return winvolobj

def createVolumeObj(search_string, content_string, condition):
    #Create the volume object
    volobj = volumeobj.VolumeObjectType()
    if search_string == "VolumeItem/DevicePath":
        volobj.set_Device_Path(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "VolumeItem/DriveLetter":
        return createWinVolumeObj(search_string, content_string, condition)
    elif search_string == "VolumeItem/Name":
        volobj.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "VolumeItem/VolumeName": #Todo - find what this means
        pass 
    elif search_string == "VolumeItem/SerialNumber":
        volobj.set_Serial_Number(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "VolumeItem/FileSystemFlags":
        file_system_flag_list = volumeobj.FileSystemFlagListType()
        file_system_flag = volumeobj.VolumeFileSystemFlagType(datatype='String', condition=condition, valueOf_=content_string)
        file_system_flag_list.add_File_System_Flag(file_system_flag)
        volobj.set_File_System_Flag_List(file_system_flag_list)
    elif search_string == "VolumeItem/ActualAvailableAllocationUnits":
        volobj.set_Actual_Available_Allocation_Units(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string == "VolumeItem/TotalAllocationUnits":
        volobj.set_Total_Allocation_Units(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string == "VolumeItem/BytesPerSector":
        volobj.set_Bytes_Per_Sector(process_numerical_value(common.PositiveIntegerObjectAttributeType(datatype='PositiveInteger'), content_string, condition))
    elif search_string == "VolumeItem/SectorsPerAllocationUnit":
        volobj.set_Sectors_Per_Allocation_Unit(process_numerical_value(common.UnsignedIntegerObjectAttributeType(datatype='UnsignedInt'), content_string, condition))
    elif search_string == "VolumeItem/CreationTime":
        volobj.set_Creation_Time(common.DateObjectAttributeType(datatype='Date', condition=condition, valueOf_=content_string))
    elif search_string == "VolumeItem/IsMounted":
        volobj.set_ismounted(content_string)
    volobj.set_anyAttributes_({'xsi:type' : 'VolumeObj:VolumeObjectType'})

    return volobj

    
def createServiceObj(search_string, content_string, condition):
    #Create the service object
    serviceobj = winserviceobj.WindowsServiceObjectType()
    if search_string == "ServiceItem/name":
        serviceobj.set_Service_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/descriptiveName": #Todo - find what this means
        pass
    elif search_string == "ServiceItem/description":
        description_list = winserviceobj.ServiceDescriptionListType()
        description_list.add_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        serviceobj.set_Description_List(description_list)    
    elif search_string == "ServiceItem/startedAs":
        serviceobj.set_Started_As(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/serviceDLL":
        serviceobj.set_Service_DLL(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/mode":
        serviceobj.set_Startup_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/pid":
        return createProcessObj(search_string, content_string, condition)
    elif search_string == "ServiceItem/status":
        serviceobj.set_Service_Status(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/path":
        return createProcessObj(search_string, content_string, condition)
    elif search_string == "ServiceItem/arguments":
        serviceobj.set_Startup_Command_Line(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/type":
        serviceobj.set_Service_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/serviceDLLmd5sum":
        service_dll_hashes = common.HashListType()
        md5hash = common.HashType()
        md5hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='MD5'))
        md5hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        service_dll_hashes.add_Hash(md5hash)
        serviceobj.set_Service_DLL_Hashes(service_dll_hashes)
    elif search_string == "ServiceItem/serviceDLLsha1sum":
        service_dll_hashes = common.HashListType()
        sha1hash = common.HashType()
        sha1hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA1'))
        sha1hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        service_dll_hashes.add_Hash(sha1hash)
        serviceobj.set_Service_DLL_Hashes(service_dll_hashes)
    elif search_string == "ServiceItem/serviceDLLsha256sum":
        service_dll_hashes = common.HashListType()
        sha256hash = common.HashType()
        sha256hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA256'))
        sha256hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        service_dll_hashes.add_Hash(sha256hash)
        serviceobj.set_Service_DLL_Hashes(service_dll_hashes)
    elif search_string == "ServiceItem/serviceDLLCertificateSubject":
        serviceobj.set_Service_DLL_Certificate_Subject(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/serviceDLLCertificateIssuer":
        serviceobj.set_Service_DLL_Certificate_Issuer(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ServiceItem/serviceDLLSignatureExists":
        serviceobj.set_service_dll_signature_exists(content_string)
    elif search_string == "ServiceItem/serviceDLLSignatureVerified":
        serviceobj.set_service_dll_signature_verified(content_string)
    elif search_string == "ServiceItem/serviceDLLSignatureDescription":
        serviceobj.set_Service_DLL_Signature_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    serviceobj.set_anyAttributes_({'xsi:type' : 'WinServiceObj:WindowsServiceObjectType'})

    return serviceobj

def createUnixFileObj(search_string, content_string, condition):
    #Create the unix file object
    fileobj = unixfileobj.UnixFileObjectType()
    if search_string == "FileItem/INode":
        fileobj.set_INode(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    fileobj.set_anyAttributes_({'xsi:type' : 'UnixFileObj:UnixFileObjectType'})
    
    return fileobj
    
def createWinFileObj(search_string, content_string, condition):
    #Create the windows file object
    fileobj = winfileobj.WindowsFileObjectType()
    if search_string == "FileItem/SecurityID":
        fileobj.set_Security_ID(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/SecurityType": #Todo - find how IOC represents this
        fileobj.set_Security_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/StreamList/Stream/Md5sum":
        stream_list = winfileobj.StreamListType()
        stream = winfileobj.StreamObjectType()
        md5hash = common.HashType()
        md5hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='MD5'))
        md5hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        stream.add_Hash(md5hash)
        stream_list.add_Stream(stream)
        fileobj.set_Stream_List(stream_list)
    elif search_string == "FileItem/StreamList/Stream/Name":
        stream_list = winfileobj.StreamListType()
        stream = winfileobj.StreamObjectType()
        stream.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        stream_list.add_Stream(stream)
        fileobj.set_Stream_List(stream_list)
    elif search_string == "FileItem/StreamList/Stream/Sha1sum":
        stream_list = winfileobj.StreamListType()
        stream = winfileobj.StreamObjectType()
        sha1hash = common.HashType()
        sha1hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA1'))
        sha1hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        stream.add_Hash(sha1hash)
        stream_list.add_Stream(stream)
        fileobj.set_Stream_List(stream_list)
    elif search_string == "FileItem/StreamList/Stream/Sha256sum":
        stream_list = winfileobj.StreamListType()
        stream = winfileobj.StreamObjectType()
        sha256hash = common.HashType()
        sha256hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA256'))
        sha256hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        stream.add_Hash(sha256hash)
        stream_list.add_Stream(stream)
        fileobj.set_Stream_List(stream_list)
    elif search_string == "FileItem/StreamList/Stream/SizeInBytes":
        stream_list = winfileobj.StreamListType()
        stream = winfileobj.StreamObjectType()
        stream.set_Size_In_Bytes(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        stream_list.add_Stream(stream)
        fileobj.set_Stream_List(stream_list)
    elif search_string == "FileItem/Drive": 
        fileobj.set_Drive(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/FilenameAccessed": 
        fileobj.set_Filename_Accessed_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/FilenameCreated": 
        fileobj.set_Filename_Created_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/FilenameModified": 
        fileobj.set_Filename_Modified_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    fileobj.set_anyAttributes_({'xsi:type' : 'WinFileObj:WindowsFileObjectType'})
    
    return fileobj
        
def createFileObj(search_string, content_string, condition):
    #Create the file object
    fleobj = fileobj.FileObjectType()    
    if search_string == "FileItem/DevicePath":
        fleobj.set_Device_Path(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/FullPath":
        fleobj.set_File_Path(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/Drive":
        return createWinFile(search_string, content_string, condition)
    elif search_string == "FileItem/FilePath":
        fleobj.set_File_Path(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/FileName":
        fleobj.set_File_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/FileExtension":
        fleobj.set_File_Extension(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/SizeInBytes":
        fleobj.set_Size_In_Bytes(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string == "FileItem/Created":
        fleobj.set_Created_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/Modified":
        fleobj.set_Modified_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/Accessed":
        fleobj.set_Accessed_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/FilenameCreated":
        return createWinFile(search_string, content_string, condition)
    elif search_string == "FileItem/FilenameModified":
        return createWinFile(search_string, content_string, condition)
    elif search_string == "FileItem/FilenameAccessed":
        return createWinFile(search_string, content_string, condition)
    elif search_string == "FileItem/FileAttributes": #Todo - restructure this in cybox
        pass
    elif search_string == "FileItem/Username":
        fleobj.set_User_Owner(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/PeakEntropy": #Todo - find how IOC represents this
        fleobj.set_Peak_Entropy(common.DoubleObjectAttributeType(datatype='Double', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/PeakCodeEntropy": #Todo - find what this means and how it's represented
        pass
    elif search_string == "FileItem/StringList/string":
        extracted_features = common.ExtractedFeaturesType()
        strings = common.ExtractedStringsType()
        string  = common.ExtractedStringType()
        string.set_String_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        strings.add_String(string)
        extracted_features.set_Strings(strings)
        fleobj.set_Extracted_Features(extracted_features)       
    elif search_string == "FileItem/INode":
        return createUnixFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/SecurityID":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/SecurityType":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/StreamList/Stream/Md5sum":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/StreamList/Stream/Name":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/StreamList/Stream/Sha1sum":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/StreamList/Stream/Sha256sum":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/StreamList/Stream/SizeInBytes":
        return createWinFileObj(search_string, content_string, condition)
    elif search_string == "FileItem/Md5sum":
        hashes = common.HashListType()
        md5hash = common.HashType()
        md5hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='MD5'))
        md5hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        hashes.add_Hash(md5hash)
        fleobj.set_Hashes(hashes)
    elif search_string == "FileItem/Sha1sum":
        hashes = common.HashListType()
        sha1hash = common.HashType()
        sha1hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA1'))
        sha1hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        hashes.add_Hash(sha1hash)
        fleobj.set_Hashes(hashes)
    elif search_string == "FileItem/Sha256sum":
        hashes = common.HashListType()
        sha256hash = common.HashType()
        sha256hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA256'))
        sha256hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        hashes.add_Hash(sha256hash)
        fleobj.set_Hashes(hashes)
    elif search_string.count('PEInfo') > 0:
        return createWinExecObj(search_string, content_string, condition)
    fleobj.set_anyAttributes_({'xsi:type' : 'FileObj:FileObjectType'})
    
    return fleobj

def createWinExecObj(search_string, content_string, condition):
    #Create the windows executable file object
    winexecobj = winexecfileobj.WindowsExecutableFileObjectType()
    pe_attributes = winexecfileobj.PEAttributesType()
    if search_string == "FileItem/PEInfo/ImportedModules/Module/ImportedFunctions/string":
        imports = winexecfileobj.PEImportListType()
        imprt = winexecfileobj.PEImportType()
        imprt_functions = winexecfileobj.PEImportedFunctionsType()
        imprt_function = winexecfileobj.PEImportedFunctionType()
        imprt_function.set_Function_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        imprt_functions.add_Imported_Function(imprt_function)
        imprt.set_Imported_Functions(imprt_functions)
        imports.add_Import(imprt)
        pe_attributes.set_Imports(imports)
    elif search_string == "FileItem/PEInfo/PETimeStamp":
        pe_attributes.set_PE_Timestamp(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "FileItem/PEInfo/BaseAddress":
        pe_attributes.set_Base_Address(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
    elif search_string == "FileItem/PEInfo/DetectedAnomalies/string": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/DetectedEntryPointSignature/Name": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/DetectedEntryPointSignature/Type": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/DigitalSignature/CertificateIssuer":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Certificate_Issuer(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        pe_attributes.set_Digital_Signature(digital_signature)
    elif search_string == "FileItem/PEInfo/DigitalSignature/CertificateSubject":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Certificate_Subject(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        pe_attributes.set_Digital_Signature(digital_signature)
    elif search_string == "FileItem/PEInfo/DigitalSignature/Description":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Signature_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        pe_attributes.set_Digital_Signature(digital_signature)
    elif search_string == "FileItem/PEInfo/DigitalSignature/SignatureExists":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_signature_exists(content_string)
        pe_attributes.set_Digital_Signature(digital_signature)
    elif search_string == "FileItem/PEInfo/DigitalSignature/SignatureVerified":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_signature_verified(content_string)
        pe_attributes.set_Digital_Signature(digital_signature)
    elif search_string == "FileItem/PEInfo/EpJumpCodes/Depth": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/EpJumpCodes/Opcodes": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/Exports/ExportedFunctions/string":
        exports = winexecfileobj.PEExportsType()
        export_functions = winexecfileobj.PEExportedFunctionsType()
        export_function = winexecfileobj.PEExportedFunctionType()
        export_function.set_Function_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        export_functions.add_Exported_Function(export_function)
        exports.set_Exported_Functions(export_functions)
        pe_attributes.set_Exports(exports)
    elif search_string == "FileItem/PEInfo/Exports/ExportsTimeStamp":
        exports = winexecfileobj.PEExportsType()
        exports.set_Exports_Time_Stamp(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
        pe_attributes.set_Exports(exports)
    elif search_string == "FileItem/PEInfo/Exports/NumberOfFunctions": #Todo - add this to CybOX?
        pass 
    elif search_string == "FileItem/PEInfo/Exports/NumberOfNames":
        exports = winexecfileobj.PEExportsType()
        exports.set_Number_Of_Names(common.LongObjectAttributeType(datatype='Long', condition=condition, valueOf_=content_string))
        pe_attributes.set_Exports(exports)
    elif search_string == "FileItem/PEInfo/ExtraneousBytes":
        pe_attributes.set_Extraneous_Bytes(process_numerical_value(common.IntegerObjectAttributeType(datatype='Int'), content_string, condition))
    elif search_string == "FileItem/PEInfo/ImportedModules/Module/Name":
        imports = winexecfileobj.PEImportListType()
        imprt = winexecfileobj.PEImportType(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        imprt.set_File_Name()
        imports.add_Import(imprt)
        pe_attributes.set_Imports(imports)
    elif search_string == "FileItem/PEInfo/PEChecksum/PEComputedAPI": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/PEChecksum/PEFileAPI": #Todo - determine what this means
        pass 
    elif search_string == "FileItem/PEInfo/PEChecksum/PEFileRaw": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/ResourceInfoList/ResourceInfoItem/Data": #Todo - add this to CybOX?
        pass 
    elif search_string == "FileItem/PEInfo/ResourceInfoList/ResourceInfoItem/Language": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/ResourceInfoList/ResourceInfoItem/Name":
        resources = winexecfileobj.PEResourceListType()
        resource = winexecfileobj.PEResourceType()
        resource.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        resources.add_Resource(resource)
        pe_attributes.set_Resources(resources)
    elif search_string == "FileItem/PEInfo/ResourceInfoList/ResourceInfoItem/Size": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/ResourceInfoList/ResourceInfoItem/Type":
        resources = winexecfileobj.PEResourceListType()
        resource = winexecfileobj.PEResourceType()
        resource.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        resources.add_Resource(resource)
        pe_attributes.set_Resources(resources)
    elif search_string == "FileItem/PEInfo/Sections/Section/DetectedCharacteristics":
        sections = winexecfileobj.PESectionListType()
        section = winexecfileobj.PESectionType()
        section_header = winexecfileobj.PESectionHeaderStructType()
        section_header.set_Characteristics(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        section.set_Section_Header(section_header)
        sections.add_Section(section)
        pe_attributes.set_Sections(sections)
    elif search_string == "FileItem/PEInfo/Sections/Section/DetectedSignatureKeys/string": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/Sections/Section/Entropy/CurveData/float": #Todo - determine what this means
        pass
    elif search_string == "FileItem/PEInfo/Sections/Section/Name":
        sections = winexecfileobj.PESectionListType()
        section = winexecfileobj.PESectionType()
        section_header = winexecfileobj.PESectionHeaderStructType()
        section_header.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        section.set_Section_Header(section_header)
        sections.add_Section(section)
        pe_attributes.set_Sections(sections)
    elif search_string == "FileItem/PEInfo/Sections/Section/SizeInBytes":
        sections = winexecfileobj.PESectionListType()
        section = winexecfileobj.PESectionType()
        section_header = winexecfileobj.PESectionHeaderStructType()
        section_header.set_Size_Of_Raw_Data(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        section.set_Section_Header(section_header)
        sections.add_Section(section)
        pe_attributes.set_Sections(sections)
    elif search_string == "FileItem/PEInfo/Sections/Section/Type":
        sections = winexecfileobj.PESectionListType()
        section = winexecfileobj.PESectionType()
        section.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        sections.add_Section(section)
        pe_attributes.set_Sections(sections)
    elif search_string == "FileItem/PEInfo/Subsystem":
        pe_attributes.set_Subsystem(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/PEInfo/Type":
        pe_attributes.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/Comments": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/CompanyName": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/FileDescription": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/FileVersion": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/InternalName": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/Language": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/LegalCopyright": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/LegalTrademarks": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/OriginalFilename": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/PrivateBuild": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/ProductName": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/ProductVersion": #Todo - add this to CybOX?
        pass
    elif search_string == "FileItem/PEInfo/VersionInfoList/VersionInfoItem/SpecialBuild": #Todo - add this to CybOX?
        pass
    winexecobj.set_PE_Attributes(pe_attributes)
    winexecobj.set_anyAttributes_({'xsi:type' : 'WinExecutableFileObj:WindowsExecutableFileObjectType'})
    
    return winexecobj

def createHookObj(search_string, content_string, condition):
    #Create the hook object
    hookobject = hookobj.WindowsKernelHookObjectType()
    if search_string ==  "HookItem/HookDescription":
        hookobject.set_Hook_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "HookItem/HookedFunction":
        hookobject.set_Hooked_Function(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "HookItem/HookedModule":
        hookobject.set_Hooked_Module(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "HookItem/HookingModule":
        hookobject.set_Hooking_Module(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "HookItem/HookingAddress":
        hookobject.set_Hooking_Address(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "HookItem/DigitalSignatureHooking/CertificateSubject":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Certificate_Subject(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        hookobject.set_Digital_Signature_Hooking(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooking/CertificateIssuer":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Certificate_Subject(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        hookobject.set_Digital_Signature_Hooking(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooking/Description":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Signature_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        hookobject.set_Digital_Signature_Hooking(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooking/SignatureExists":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.signature_exists(content_string)
        hookobject.set_Digital_Signature_Hooking(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooking/SignatureVerified":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.signature_verified(content_string)
        hookobject.set_Digital_Signature_Hooking(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooked/CertificateSubject":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Certificate_Subject(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        hookobject.set_Digital_Signature_Hooked(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooked/CertificateIssuer":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Certificate_Subject(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        hookobject.set_Digital_Signature_Hooked(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooked/Description":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.set_Signature_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        hookobject.set_Digital_Signature_Hooked(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooked/SignatureExists":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.signature_exists(content_string)
        hookobject.set_Digital_Signature_Hooked(digital_signature)
    elif search_string ==  "HookItem/DigitalSignatureHooked/SignatureVerified":
        digital_signature = common.DigitalSignatureInfoType()
        digital_signature.signature_verified(content_string)
        hookobject.set_Digital_Signature_Hooked(digital_signature)
    hookobject.set_anyAttributes_({'xsi:type' : 'WinKernelHookObj:WindowsKernelHookObjectType'})
    
    return hookobject

def createDriverObj(search_string, content_string, condition):
    #Create the driver object
    driverobj = windriverobj.WindowsDriverObjectType()
    if search_string ==  "DriverItem/DriverObjectAddress":
        driverobj.set_Driver_Object_Address(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
    elif search_string ==  "DriverItem/ImageSize":
        driverobj.set_Image_Size(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))  
    elif search_string ==  "DriverItem/ImageBase":
        driverobj.set_Image_Base(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))  
    elif search_string ==  "DriverItem/DriverName":
        driverobj.set_Driver_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=content_string))
    elif search_string ==  "DriverItem/DriverInit":
        driverobj.set_Driver_Init(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/DriverStartIo":
        driverobj.set_Driver_Start_IO(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
    elif search_string ==  "DriverItem/DriverUnload":
        driverobj.set_Driver_Unload(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_CREATE":
        driverobj.set_IRP_MJ_CREATE(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_CLOSE":
        driverobj.set_IRP_MJ_CLOSE(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_WRITE":
        driverobj.set_IRP_MJ_WRITE(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_READ":
        driverobj.set_IRP_MJ_READ(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_QUERY_INFORMATION":
        driverobj.set_IRP_MJ_QUERY_INFORMATION(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SET_INFORMATION":
        driverobj.set_IRP_MJ_SET_INFORMATION(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_QUERY_EA":
        driverobj.set_IRP_MJ_QUERY_EA(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SET_EA":
        driverobj.set_IRP_MJ_SET_EA(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_FLUSH_BUFFERS":
        driverobj.set_IRP_MJ_FLUSH_BUFFERS(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_QUERY_VOLUME_INFORMATION":
        driverobj.set_IRP_MJ_QUERY_VOLUME_INFORMATION(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SET_VOLUME_INFORMATION":
        driverobj.set_IRP_MJ_SET_VOLUME_INFORMATION(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_DIRECTORY_CONTROL":
        driverobj.set_IRP_MJ_DIRECTORY_CONTROL(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_FILE_SYSTEM_CONTROL":
        driverobj.set_IRP_MJ_FILE_SYSTEM_CONTROL(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_DIRECTORY_CONTROL":
        driverobj.set_IRP_MJ_DIRECTORY_CONTROL(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_INTERNAL_DEVICE_CONTROL":
        driverobj.set_IRP_MJ_INTERNAL_DEVICE_CONTROL(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SHUTDOWN":
        driverobj.set_IRP_MJ_SHUTDOWN(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_LOCK_CONTROL":
        driverobj.set_IRP_MJ_LOCK_CONTROL(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_CLEANUP":
        driverobj.set_IRP_MJ_CLEANUP(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_CREATE_MAILSLOT":
        driverobj.set_IRP_MJ_CREATE_MAILSLOT(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_QUERY_SECURITY":
        driverobj.set_IRP_MJ_QUERY_SECURITY(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SET_SECURITY":
        driverobj.set_IRP_MJ_SET_SECURITY(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_POWER":
        driverobj.set_IRP_MJ_POWER(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SYSTEM_CONTROL":
        driverobj.set_IRP_MJ_SYSTEM_CONTROL(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_DEVICE_CHANGE":
        driverobj.set_IRP_MJ_DEVICE_CHANGE(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_QUERY_QUOTA":
        driverobj.set_IRP_MJ_QUERY_QUOTA(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_SET_QUOTA":
        driverobj.set_IRP_MJ_SET_QUOTA(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_PNP":
        driverobj.set_IRP_MJ_PNP(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/IRP_MJ_CREATE_NAMED_PIPE":
        driverobj.set_IRP_MJ_CREATE_NAMED_PIPE(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
    elif search_string ==  "DriverItem/DeviceItem/DeviceObject":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Device_Object(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/DeviceName":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Device_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/DriverName":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Driver_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/AttachedDeviceObject":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Attached_Device_Object(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/AttachedDeviceName":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Attached_Device_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/AttachedDriverObject": #TODO - figure out what this means
        pass
    elif search_string ==  "DriverItem/DeviceItem/AttachedDriverName": #TODO - figure out what this means
        pass
    elif search_string ==  "DriverItem/DeviceItem/AttachedToDeviceObject":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Attached_To_Device_Object(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/AttachedToDeviceName":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Attached_To_Device_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/AttachedToDriverObject":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.get_Attached_To_Driver_Object(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)
    elif search_string ==  "DriverItem/DeviceItem/AttachedToDriverName":
        device_list = windriverobj.DeviceObjectListType()
        device_object = windriverobj.DeviceObjectType()
        device_object.set_Attached_To_Driver_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=content_string))
        device_list.add_Device_Object(device_object)
        driverobj.set_Device_Object_List(device_list)

    driverobj.set_anyAttributes_({'xsi:type' : 'WinDriverObj:WindowsDriverObjectType'})
    
    return driverobj

def createPortObj(search_string, content_string, condition):
    #Create the port object
    portobject = portobj.PortObjectType()
    if search_string == "PortItem/localPort" or search_string == "PortItem/remotePort":
        portobject.set_Port_Value(process_numerical_value(common.PositiveIntegerObjectAttributeType(datatype='PositiveInteger'), content_string, condition))
    elif search_string ==  "PortItem/protocol":
        portobject.set_Layer4_Protocol(stringobjattribute)
    portobject.set_anyAttributes_({'xsi:type' : 'PortObj:PortObjectType'})
    
    return portobject

def createRegObj(search_string, content_string, condition): 
    #Create the registry object
    regobj = winregobj.WindowsRegistryKeyObjectType()
    if search_string ==  "RegistryItem/Type":
        values = winregobj.RegistryValuesType()
        value = winregobj.RegistryValueType()
        value.set_Datatype(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        values.add_Value(value)
        regobj.set_Values(values)
    elif search_string ==  "RegistryItem/Modified":
        regobj.set_Modified_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string ==  "RegistryItem/NumSubKeys":
        regobj.set_Number_Subkeys(process_numerical_value(common.UnsignedIntegerObjectAttributeType(datatype='UnsignedInt'), content_string, condition))
    elif search_string ==  "RegistryItem/NumValues":
        regobj.set_Number_Values(process_numerical_value(common.UnsignedIntegerObjectAttributeType(datatype='UnsignedInt'), content_string, condition))
    elif search_string ==  "RegistryItem/Hive":
        regobj.set_Hive(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "RegistryItem/Username":
        regobj.set_Creator_Username(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "RegistryItem/ValueName":
        values = winregobj.RegistryValuesType()
        value = winregobj.RegistryValueType()
        value.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        values.add_Value(value)
        regobj.set_Values(values)
    elif search_string == "RegistryItem/Text" or search_string == "RegistryItem/Value":
        values = winregobj.RegistryValuesType()
        value = winregobj.RegistryValueType()
        value.set_Data(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        values.add_Value(value)
        regobj.set_Values(values)
    elif search_string ==  "RegistryItem/KeyPath":
        regobj.set_Key(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "RegistryItem/Path":
        split_path = content_string.split('\\', 1)
        regobj.set_Hive(common.StringObjectAttributeType(datatype='String', condition='Equals', valueOf_=split_path[0]))
        regobj.set_Key(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=split_path[1]))
    regobj.set_anyAttributes_({'xsi:type' : 'WinRegistryKeyObj:WindowsRegistryKeyObjectType'})
    
    return regobj

def createWinUserObj(search_string, content_string, condition):
    #Create the win user account object
    accountobj = winuseraccountobj.WindowsUserAccountObjectType()
    if search_string ==  "UserItem/SecurityID":
        accountobj.set_Security_ID(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "UserItem/SecurityType":
        accountobj.set_Security_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    accountobj.set_anyAttributes_({'xsi:type' : 'WinUserAccountObj:WindowsUserAccountObjectType'})
    
    return accountobj

def createAccountObj(search_string, content_string, condition):
    #Create the account object
    accountobj = accountobj.AccountObjectType()
    if search_string ==  "UserItem/description":
        accountobj.set_Description(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "UserItem/disabled":
        accountobj.set_disabled(content_string)
    elif search_string ==  "UserItem/lockedout":
        accountobj.set_locked_out(content_string)
    accountobj.set_anyAttributes_({'xsi:type' : 'AccountObj:AccountObjectType'})
    
    return accountobj
    
def createUserObj(search_string, content_string, condition):
    #Create the user account object
    accountobj = useraccountobj.UserAccountObjectType()
    if search_string ==  "UserItem/Username":
        accountobj.set_Username(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "UserItem/fullname":
        accountobj.set_Full_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "UserItem/grouplist/groupname":
        group_list = useraccountobj.GroupListType()
        group = winuseraccountobj.WindowsGroupType()
        group.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        group_list.add_Group(group)
        accountobj.set_Group_List(group_list)
    elif search_string ==  "UserItem/LastLogin":
        accountobj.set_Last_Login(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string ==  "UserItem/passwordrequired":
        accountobj.set_password_required(content_string)
    elif search_string ==  "UserItem/userpasswordage":
        accountobj.set_User_Password_Age(common.DurationObjectAttributeType(datatype='Duration', condition=condition, valueOf_=content_string))
    elif search_string ==  "UserItem/homedirectory":
        accountobj.set_Home_Directory(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string ==  "UserItem/description":
        return createAccountObj(search_string, content_string, condition)
    elif search_string ==  "UserItem/SecurityID":
        return createWinUserObj(search_string, content_string, condition)
    elif search_string ==  "UserItem/SecurityType":
        return createWinUserObj(search_string, content_string, condition)
    elif search_string ==  "UserItem/disabled":
        return createAccountObj(search_string, content_string, condition)
    elif search_string ==  "UserItem/lockedout":
        return createAccountObj(search_string, content_string, condition)
    elif search_string ==  "UserItem/scriptpath":
        accountobj.set_Script_path(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    accountobj.set_anyAttributes_({'xsi:type' : 'UserAccountObj:UserAccountObjectType'})
    
    return accountobj
    
def createWinEventLogObj(search_string, content_string, condition):
    #Create the Win event log object
    eventlogobj = wineventlogobj.WindowsEventLogObjectType()
    if search_string == "EventLogItem/EID":
        eventlogobj.set_EID(common.LongObjectAttributeType(datatype='Long', condition=condition, valueOf_=content_string))
    elif search_string == "EventLogItem/log":
        eventlogobj.set_Log(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/CorrelationActivityId":
        eventlogobj.set_Correlation_Activity_ID(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/CorrelationRelatedActivityId":
        eventlogobj.set_Correlation_Related_Activity_ID(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/ExecutionProcessId":
        eventlogobj.set_Execution_Process_ID(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/ExecutionThreadId":
        eventlogobj.set_Execution_Thread_ID(stringobjattribute)
    elif search_string == "EventLogItem/index":
        eventlogobj.set_Index(common.LongObjectAttributeType(datatype='Long', condition=condition, valueOf_=content_string))
    elif search_string == "EventLogItem/type":
        eventlogobj.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/categoryNum":
        eventlogobj.set_Category_Num(common.LongObjectAttributeType(datatype='Long', condition=condition, valueOf_=content_string))
    elif search_string == "EventLogItem/genTime":
        eventlogobj.set_Generation_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "EventLogItem/writeTime":
        eventlogobj.set_Write_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "EventLogItem/reserved":
        eventlogobj.set_Reserved(common.LongObjectAttributeType(datatype='Long', condition=condition, valueOf_=content_string))
    elif search_string == "EventLogItem/source":
        eventlogobj.set_Source(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/machine":
        eventlogobj.set_Machine(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/user":
        eventlogobj.set_User(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/category":
        eventlogobj.set_Category(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/message":
        eventlogobj.set_Message(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "EventLogItem/unformattedMessage/string":
        unformatted_message_list = wineventlogobj.UnformattedMessageListType()
        unformatted_message_list.add_Unformatted_Message(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        eventlogobj.set_Unformatted_Message_List(unformatted_message_list)
    elif search_string == "EventLogItem/blob":
        eventlogobj.set_Blob(common.Base64BinaryObjectAttributeType(datatype='Base64Binary', condition=condition, valueOf_=content_string))
    eventlogobj.set_anyAttributes_({'xsi:type' : 'WinEventLogObj:WindowsEventLogObjectType'})
    
    return eventlogobj
    
def createWinProcessObj(search_string, content_string, condition):
    #Create the Win process object
    winprocobj = winprocessobj.WindowsProcessObjectType()
    if search_string == "ProcessItem/SecurityID":
        winprocobj.set_Security_ID(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ProcessItem/SecurityType":
        winprocobj.set_Security_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ProcessItem/HandleList/Handle/Name":
        handle_list = winhandleobj.WindowsHandleListType()
        handle = winhandleobj.WindowsHandleObjectType()
        handle.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        handle_list.add_Handle(handle)
        winprocobj.set_Handle_List(handle_list)
    elif search_string == "ProcessItem/HandleList/Handle/AccessMask":
        handle_list = winhandleobj.WindowsHandleListType()
        handle = winhandleobj.WindowsHandleObjectType()
        handle.set_Access_Mask(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        handle_list.add_Handle(handle)
        winprocobj.set_Handle_List(handle_list) 
    elif search_string == "ProcessItem/HandleList/Handle/HandleCount": #Todo - add this to CybOX?
        pass
    elif search_string == "ProcessItem/HandleList/Handle/Index":
        handle_list = winhandleobj.WindowsHandleListType()
        handle = winhandleobj.WindowsHandleObjectType()
        handle.set_ID(process_numerical_value(common.UnsignedIntegerObjectAttributeType(datatype='UnsignedInt'), content_string, condition))
        handle_list.add_Handle(handle)
        winprocobj.set_Handle_List(handle_list)
    elif search_string == "ProcessItem/HandleList/Handle/ObjectAddress":
        handle_list = winhandleobj.WindowsHandleListType()
        handle = winhandleobj.WindowsHandleObjectType()
        handle.set_Object_Address(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        handle_list.add_Handle(handle)
        winprocobj.set_Handle_List(handle_list)
    elif search_string == "ProcessItem/HandleList/Handle/PointerCount":
        handle_list = winhandleobj.WindowsHandleListType()
        handle = winhandleobj.WindowsHandleObjectType()
        handle.set_Pointer_Count(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        handle_list.add_Handle(handle)
        winprocobj.set_Handle_List(handle_list)
    elif search_string == "ProcessItem/HandleList/Handle/Type":
        handle_list = winhandleobj.WindowsHandleListType()
        handle = winhandleobj.WindowsHandleObjectType()
        handle.set_Type(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        handle_list.add_Handle(handle)
        winprocobj.set_Handle_List(handle_list)
    elif search_string == "ProcessItem/SectionList/MemorySection/Injected":
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_is_injected(content_string)
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(memory_section_list)
    elif search_string == "ProcessItem/SectionList/MemorySection/Mapped":
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_is_mapped(content_string)
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(memory_section_list)
    elif search_string == "ProcessItem/SectionList/MemorySection/MD5Sum":
        hashes = common.HashListType()
        md5hash = common.HashType()
        md5hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='MD5'))
        md5hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        hashes.add_Hash(md5hash)
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_Hashes(hashes)
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(stringobjattribute)
    elif search_string == "ProcessItem/SectionList/MemorySection/Sha1Sum":
        hashes = common.HashListType()
        sha1hash = common.HashType()
        sha1hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA1'))
        sha1hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        hashes.add_Hash(sha1hash)
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_Hashes(hashes)
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(stringobjattribute)
        winprocobj.set_Section_List(stringobjattribute)
    elif search_string == "ProcessItem/SectionList/MemorySection/Sha256Sum":
        hashes = common.HashListType()
        sha256hash = common.HashType()
        sha256hash.set_Type(common.StringObjectAttributeType(datatype='String', valueOf_='SHA256'))
        sha256hash.set_Simple_Hash_Value(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        hashes.add_Hash(sha256hash)
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_Hashes(hashes)
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(stringobjattribute)
        winprocobj.set_Section_List(stringobjattribute)
    elif search_string == "ProcessItem/SectionList/MemorySection/Name":
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(memory_section_list)
    elif search_string == "ProcessItem/SectionList/MemorySection/Protection": #Todo - find what this means and how it's represented
        pass
    elif search_string == "ProcessItem/SectionList/MemorySection/RawFlags": #Todo - find what this means and how it's represented
        pass 
    elif search_string == "ProcessItem/SectionList/MemorySection/RegionSize":
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_Region_Size(process_numerical_value(common.UnsignedLongObjectAttributeType(datatype='UnsignedLong'), content_string, condition))
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(memory_section_list)
    elif search_string == "ProcessItem/SectionList/MemorySection/RegionStart":
        memory_section_list = winprocessobj.MemorySectionListType()
        memory_section = memoryobj.MemoryObjectType()
        memory_section.set_Region_Start_Address(process_numerical_value(common.HexBinaryObjectAttributeType(datatype='hexBinary'), content_string, condition))
        memory_section_list.add_Memory_Section(memory_section)
        winprocobj.set_Section_List(memory_section_list)
    winprocobj.set_anyAttributes_({'xsi:type' : 'WinProcessObj:WindowsProcessObjectType'})

    return winprocobj
    
def createProcessObj(search_string, content_string, condition):
    #Create the process object
    procobj = processobj.ProcessObjectType()
    if search_string == "ProcessItem/name":
        procobj.set_Name(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ProcessItem/pid":
        procobj.set_PID(process_numerical_value(common.UnsignedIntegerObjectAttributeType(datatype='UnsignedInt'), content_string, condition))
    elif search_string == "ProcessItem/parentpid":
        procobj.set_Parent_PID(process_numerical_value(common.UnsignedIntegerObjectAttributeType(datatype='UnsignedInt'), content_string, condition))
    elif search_string == "ProcessItem/Username":
        procobj.set_Username(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
    elif search_string == "ProcessItem/startTime":
        procobj.set_Start_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
    elif search_string == "ProcessItem/path":
        image_info = processobj.ImageInfoType()
        image_info.set_Path(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        procobj.set_Image_Info(image_info)
    elif search_string == "ProcessItem/userTime":
        procobj.set_User_Time(common.DurationObjectAttributeType(datatype='Duration', condition=condition, valueOf_=content_string))
    elif search_string == "ProcessItem/StringList/string":
        string_list = common.ExtractedStringsType()
        string = common.ExtractedStringType()
        string.set_String_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        string_list.add_String(string)
        procobj.set_String_List(string_list)
    elif search_string == "ProcessItem/hidden":
        procobj.set_is_hidden(content_string)
    elif search_string == "ProcessItem/arguments":
        image_info = processobj.ImageInfoType()
        image_info.set_Command_Line(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        procobj.set_Image_Info(image_info)
    elif search_string == "ProcessItem/PortList/PortItem/CreationTime":
        netconn_list = processobj.NetworkConnectionListType()
        netconn = processobj.NetworkConnectionType()
        netconn.set_Creation_Time(common.DateTimeObjectAttributeType(datatype='DateTime', condition=condition, valueOf_=content_string))
        netconn_list.add_Network_Connection(netconn)
        procobj.set_Network_Connection_List(netconn_list)
    elif search_string == "ProcessItem/PortList/PortItem/localIP":
        netconn_list = processobj.NetworkConnectionListType()
        netconn = processobj.NetworkConnectionType()
        local_ip = addressobj.AddressObjectType(category='ipv4-addr')
        local_ip.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netconn.set_Source_IP_Address(local_ip)
        netconn_list.add_Network_Connection(netconn)
        procobj.set_Network_Connection_List(netconn_list)
    elif search_string == "ProcessItem/PortList/PortItem/localPort":
        netconn_list = processobj.NetworkConnectionListType()
        netconn = processobj.NetworkConnectionType()
        local_port = portobj.PortObjectType()
        local_port.set_Port_Value(process_numerical_value(common.PositiveIntegerObjectAttributeType(datatype='PositiveInteger'), content_string, condition))
        netconn.set_Source_Port(local_port)
        netconn_list.add_Network_Connection(netconn)
        procobj.set_Network_Connection_List(netconn_list)
    elif search_string == "ProcessItem/PortList/PortItem/path": #Todo - determine what this means
        pass
    elif search_string == "ProcessItem/PortList/PortItem/pid": #Todo - determine what this means
        pass
    elif search_string == "ProcessItem/PortList/PortItem/process": #Todo - determine what this means
        pass
    elif search_string == "ProcessItem/PortList/PortItem/protocol": #Todo - determine what this means
        pass
    elif search_string == "ProcessItem/PortList/PortItem/remoteIP":
        netconn_list = processobj.NetworkConnectionListType()
        netconn = processobj.NetworkConnectionType()
        remote_ip = addressobj.AddressObjectType(category='ipv4-addr')
        remote_ip.set_Address_Value(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netconn.set_Destination_IP_Address(remote_ip)
        netconn_list.add_Network_Connection(netconn)
        procobj.set_Network_Connection_List(netconn_list)
    elif search_string == "ProcessItem/PortList/PortItem/remotePort":
        netconn_list = processobj.NetworkConnectionListType()
        netconn = processobj.NetworkConnectionType()
        dest_port = portobj.PortObjectType()
        dest_port.set_Port_Value(process_numerical_value(common.PositiveIntegerObjectAttributeType(datatype='PositiveInteger'), content_string, condition))
        netconn.set_Destination_Port(dest_port)
        netconn_list.add_Network_Connection(netconn)
        procobj.set_Network_Connection_List(netconn_list)
    elif search_string == "ProcessItem/PortList/PortItem/state":
        netconn_list = processobj.NetworkConnectionListType()
        netconn = processobj.NetworkConnectionType()
        netconn.set_TCP_State(common.StringObjectAttributeType(datatype='String', condition=condition, valueOf_=process_string_value(content_string)))
        netconn_list.add_Network_Connection(netconn)
        procobj.set_Network_Connection_List(netconn_list)
    elif search_string == "ProcessItem/SecurityID":
        return createWinProcessObj(search_string, content_string, condition)
    elif search_string == "ProcessItem/SecurityType":
        return createWinProcessObj(search_string, content_string, condition)
    elif search_string.count("HandleList") > 0:
        return createWinProcessObj(search_string, content_string, condition)
    elif search_string.count("SectionList") > 0:
        return createWinProcessObj(search_string, content_string, condition)
    procobj.set_anyAttributes_({'xsi:type' : 'ProcessObj:ProcessObjectType'})
    
    return procobj

#Set the correct attributes for any range values
def process_numerical_value(object_attribute, content_string, condition):
    if content_string.count('[') > 0 and content_string.count('TO') > 0:
        normalized_string = content_string.strip('[]')
        split_string = normalized_string.split('TO')
        object_attribute.set_start_range(split_string[0].strip())
        object_attribute.set_end_range(split_string[1].strip())
        if condition == 'Contains' or condition == 'Equals':
            object_attribute.set_condition('IsInRange')
        elif condition == 'DoesNotContain' or condition == 'DoesNotEqual':
            object_attribute.set_condition('IsNotInRange')
    else:
        object_attribute.set_condition(condition)
        object_attribute.set_valueOf_(content_string)
    return object_attribute

#Encase any strings with XML escape characters in the proper tags
def process_string_value(content_string):
    if (
    content_string.count('<') > 0 or
    content_string.count('>') > 0 or
    content_string.count("'") > 0 or
    content_string.count('"') > 0 or
    content_string.count('&') > 0 
    ):
        return ('<![CDATA[' + content_string + ']]>')
    else:
        return content_string
