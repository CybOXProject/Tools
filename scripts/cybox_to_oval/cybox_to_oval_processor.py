#CybOX -> OVAL Translator
#v0.1 BETA
#Processor Class

# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import cybox.cybox_1_0 as cybox #bindings
import cybox.common_types_1_0 as common #bindings
import oval57 as oval #bindings
import cybox_oval_mappings
import sys
import os
import traceback
import datetime

class cybox_to_oval_processor(object):
    def __init__(self, infilename, outfilename, verbose_mode):
        self.converted_ids = []
        self.skipped_observables = []
        self.oval_defs = oval.DefinitionsType()
        self.oval_tests = oval.TestsType()
        self.oval_objects = oval.ObjectsType()
        self.oval_states = oval.StatesType()
        self.ovaldefroot = oval.oval_definitions()
        self.mappings = cybox_oval_mappings.cybox_oval_mappings()
        self.infilename = infilename
        self.outfilename = outfilename
        self.verbose_mode = verbose_mode

    #Find an observable that was referenced
    #This assumes that the reference was from inside an observable composition to an external observable
    #i.e. not one in the same observable
    def process_observable_ref(self, idref, observables):
        for observable in observables:
            if type(observable) is cybox.ObservableType and observable.id == idref:
                return observable
        return None
    
    #Process a single observable
    def process_observable(self, observable, oval_criteria, normal_observables = None):
        if observable.Stateful_Measure is not None:
            oval_entities = self.mappings.create_oval(observable.Stateful_Measure.Object.Defined_Object)
            if oval_entities is not None:
                #Add the tests, objects, and states to the oval document
                self.oval_tests.add_test(oval_entities.get('test'))
                self.oval_objects.add_object(oval_entities.get('object'))
                if oval_entities.has_key('state'):
                    for oval_state in oval_entities.get('state'):
                        self.oval_states.add_state(oval_state)
                #Create the criterion and add it to the criteria
                oval_criterion = oval.CriterionType(test_ref = oval_entities.get('test').id)
                oval_criteria.add_criterion(oval_criterion)
            else:
                if observable.id:
                    self.skipped_observables.append(observable.id)
            self.converted_ids.append(observable.id)
        if observable.Observable_Composition is not None:
            self.process_observable_composition(observable.Observable_Composition, oval_criteria, normal_observables)

    #Process a single observable composition and create the associated definition structure
    def process_observable_composition(self, observable_composition, oval_criteria, observables):
        obs_criteria = oval.CriteriaType(operator = observable_composition.get_Operator())
        for observable in observable_composition.Observable:
            if observable.id is not None and observable.id not in self.converted_ids:
                self.process_observable(observable, obs_criteria, observables)
                self.converted_ids.append(observable.id)
            elif observable.idref:
                actual_observable = self.process_observable_ref(observable.idref, observables)
                if actual_observable is not None:
                    self.process_observable(actual_observable, obs_criteria, observables)
        if obs_criteria.hasContent_():
            oval_criteria.add_criteria(obs_criteria)

    #Process the two observable bins - first those with observable compositions, then without
    def process_observables(self, obscomp_observables, normal_observables):
        metadata = oval.MetadataType(title = 'Object check', description = 'Existence check for object(s) extracted from CybOX Observable')
        for observable in obscomp_observables:
            oval_def = oval.DefinitionType(version = 1.0, id = self.mappings.generate_def_id(), classxx = 'miscellaneous', metadata = metadata)
            oval_criteria = oval.CriteriaType()
            self.process_observable(observable, oval_criteria, normal_observables)
            if oval_criteria.hasContent_():
                oval_def.set_criteria(oval_criteria)
                self.oval_defs.add_definition(oval_def)
        for observable in normal_observables:
            if observable.id not in self.converted_ids:
                oval_def = oval.DefinitionType(version = 1.0, id = self.mappings.generate_def_id(), classxx = 'miscellaneous', metadata = metadata)
                oval_criteria = oval.CriteriaType()
                self.process_observable(observable, oval_criteria)
                if oval_criteria.hasContent_():
                    oval_def.set_criteria(oval_criteria)
                    self.oval_defs.add_definition(oval_def)

    #Generate OVAL output from the CybOX observables
    def generate_oval(self):
        #Basic input file checking
        if os.path.isfile(self.infilename):    
            #Parse the cybox file
            observables = cybox.parse(self.infilename)
            try:
                sys.stdout.write('Generating ' + self.outfilename + ' from ' + self.infilename + '...')

                normal_observables = []
                obscomp_observables = []

                #Parse the observables and create their corresponding OVAL
                #Two bins: one for observables with observable compositions, and one for those without
                #This is to ensure that we account for referenced observables correctly
                for observable in observables.Observable:
                    if type(observable) is cybox.ObservableType and not observable.Observable_Composition:
                        normal_observables.append(observable)
                    elif type(observable) is cybox.ObservableType and observable.Observable_Composition:
                        obscomp_observables.append(observable)

                self.process_observables(obscomp_observables, normal_observables)

                #Build up the OVAL document from the parsed data and corresponding objects
                self.__build_oval_document()

                #Export to the output file
                outfile = open(self.outfilename, 'w')
                self.ovaldefroot.export(outfile, 0, namespacedef_='xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5" xmlns:oval-def="http://oval.mitre.org/XMLSchema/oval-definitions-5" xmlns:win-def="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" xmlns:oval="http://oval.mitre.org/XMLSchema/oval-common-5" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows http://oval.mitre.org/language/version5.7/ovaldefinition/complete/windows-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-definitions-5 http://oval.mitre.org/language/version5.7/ovaldefinition/complete/oval-definitions-schema.xsd http://oval.mitre.org/XMLSchema/oval-common-5 http://oval.mitre.org/language/version5.7/ovaldefinition/complete/oval-common-schema.xsd"')
                sys.stdout.write('Done')
                if self.verbose_mode:
                    for observable in self.skipped_observables:
                        print 'Observable ' + observable + ' skipped; incompatible object type or missing object attributes'

            except Exception, err:
                print('\nError: %s\n' % str(err))
                if self.verbose_mode:
                    traceback.print_exc()
                    for observable in self.skipped_observables:
                        print 'Observable ' + observable + ' skipped; incompatible object type or missing object attributes'
           
        else:
            print('\nError: Input file not found or inaccessible.')
            sys.exit(1)

    #Helper methods
    def __generate_datetime(self):
        dtime = datetime.datetime.now().isoformat()
        return dtime

    def __build_oval_document(self):
        #Add the generator to the defs
        oval_gen = oval.GeneratorType()
        oval_gen.set_product_name('CybOX XML to OVAL Script')
        oval_gen.set_product_version('0.1')
        oval_gen.set_schema_version('5.7')
        #Generate the datetime
        oval_gen.set_timestamp(self.__generate_datetime())

        #Add the definitions, tests, objects, and generator to the root OVAL document
        self.ovaldefroot.set_definitions(self.oval_defs)
        self.ovaldefroot.set_tests(self.oval_tests)
        self.ovaldefroot.set_objects(self.oval_objects)
        if self.oval_states.hasContent_():
            self.ovaldefroot.set_states(self.oval_states)
        self.ovaldefroot.set_generator(oval_gen)
    
