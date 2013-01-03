import cybox_core_v1 as cybox
import process_object_1_3 as process_object
import email_message_object_1_2 as email_message_object
import file_object_1_3 as file_object
import address_object_1_2 as address_object
import uri_object_1_2 as uri_object

observables = cybox.ObservablesType(cybox_minor_version = "1", cybox_major_version = "0")
observable = cybox.ObservableType(id="test-observable-1")
stateful_measure = cybox.StatefulMeasureType()
object = cybox.ObjectType(id="test-obj-1")
#win_file_obj = win_file_object.WindowsFileObjectType()
#win_file_obj.set_Device_Path(cybox.cybox_common_types_v1_0.StringObjectAttributeType(datatype='String', valueOf_='test'))
#win_file_obj.set_Filename_Accessed_Time(cybox.cybox_common_types_v1_0.DateTimeObjectAttributeType(datatype='DateTime', valueOf_='12:22:22'))
#win_file_obj.set_anyAttributes_({"xsi:type":"WinFileObj:WindowsFileObjectType"})
email_message_obj = email_message_object.EmailMessageObjectType()
email_headers = email_message_object.EmailHeaderType()
email_headers.set_From(cybox.cybox_common_types_v1_0.StringObjectAttributeType(datatype='String', valueOf_='test'))
email_headers.set_Subject(cybox.cybox_common_types_v1_0.StringObjectAttributeType(datatype='String', valueOf_='test subject'))
email_message_obj.set_Header(email_headers)
email_message_obj.set_anyAttributes_({"xsi:type":"EmailMessageObj:EmailMessageObjectType"})
#process_obj = process_object.ProcessObjectType()
#process_obj.set_anyAttributes_({"xsi:type":"ProcessObj:ProcessObjectType"})
#process_obj.set_PID(cybox.cybox_common_types_v1_0.UnsignedIntegerObjectAttributeType(valueOf_=256))
#process_obj.set_Name(cybox.cybox_common_types_v1_0.StringObjectAttributeType(valueOf_='some_process'))
object.set_Defined_Object(email_message_obj)
stateful_measure.set_Object(object)
observable.set_Stateful_Measure(stateful_measure)
observables.add_Observable(observable)
file = open('test_out_new.xml', mode='w')
observables.export(file,0)
