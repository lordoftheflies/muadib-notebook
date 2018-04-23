#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# ./manage.py dumpscript instrumentation
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: instrumentation.models.EnumerationModel

    from instrumentation.models import EnumerationModel


    # Processing model: instrumentation.models.ConstantModel

    from instrumentation.models import ConstantModel


    # Processing model: instrumentation.models.SchemaModel

    from instrumentation.models import SchemaModel

    instrumentation_schemamodel_1 = SchemaModel()
    instrumentation_schemamodel_1.distinguished_name = 'receiver'
    instrumentation_schemamodel_1.display_name = 'Mérővevő'
    instrumentation_schemamodel_1.description = 'Mérővevő séma.'
    instrumentation_schemamodel_1 = importer.save_or_locate(instrumentation_schemamodel_1)

    instrumentation_schemamodel_2 = SchemaModel()
    instrumentation_schemamodel_2.distinguished_name = 'antenna_rotator'
    instrumentation_schemamodel_2.display_name = 'Antenna forgató'
    instrumentation_schemamodel_2.description = 'Antenna fogató.'
    instrumentation_schemamodel_2 = importer.save_or_locate(instrumentation_schemamodel_2)

    instrumentation_schemamodel_3 = SchemaModel()
    instrumentation_schemamodel_3.distinguished_name = 'spectrum_analizator'
    instrumentation_schemamodel_3.display_name = 'Spektrum analizátor'
    instrumentation_schemamodel_3.description = 'Spektrum analizátor séma.'
    instrumentation_schemamodel_3 = importer.save_or_locate(instrumentation_schemamodel_3)

    # Processing model: instrumentation.models.SchemaAttributeModel

    from instrumentation.models import SchemaAttributeModel

    instrumentation_schemaattributemodel_1 = SchemaAttributeModel()
    instrumentation_schemaattributemodel_1.distinguished_name = 'frequency_f'
    instrumentation_schemaattributemodel_1.display_name = 'Vételi frekvencia'
    instrumentation_schemaattributemodel_1.description = 'Vételi frekvencia lehetséges értéke 0 Hz és 50 MHz között változhat.'
    instrumentation_schemaattributemodel_1.schema = instrumentation_schemamodel_3
    instrumentation_schemaattributemodel_1.data_type = 'float'
    instrumentation_schemaattributemodel_1.data_precision = 3
    instrumentation_schemaattributemodel_1.representation_type = 'number'
    instrumentation_schemaattributemodel_1.representation_precision = 3
    instrumentation_schemaattributemodel_1.constrait_minimum = 0.0
    instrumentation_schemaattributemodel_1.constrait_maximum = 50000000.0
    instrumentation_schemaattributemodel_1.constrait_pattern = None
    instrumentation_schemaattributemodel_1.constrait_required = True
    instrumentation_schemaattributemodel_1 = importer.save_or_locate(instrumentation_schemaattributemodel_1)

    # Processing model: instrumentation.models.EquipmentModel

    from instrumentation.models import EquipmentModel

    instrumentation_equipmentmodel_1 = EquipmentModel()
    instrumentation_equipmentmodel_1.distinguished_name = 'ek895'
    instrumentation_equipmentmodel_1.display_name = 'EK-895'
    instrumentation_equipmentmodel_1.description = 'EK-895 mérővevő.'
    instrumentation_equipmentmodel_1.schema = instrumentation_schemamodel_1
    instrumentation_equipmentmodel_1._configuration = '{}'
    instrumentation_equipmentmodel_1.address = 'GPIB0::14::INSTR'
    instrumentation_equipmentmodel_1 = importer.save_or_locate(instrumentation_equipmentmodel_1)

    instrumentation_equipmentmodel_2 = EquipmentModel()
    instrumentation_equipmentmodel_2.distinguished_name = 'esmb'
    instrumentation_equipmentmodel_2.display_name = 'ESMB'
    instrumentation_equipmentmodel_2.description = 'ESMB mérővevő.'
    instrumentation_equipmentmodel_2.schema = instrumentation_schemamodel_1
    instrumentation_equipmentmodel_2._configuration = '{}'
    instrumentation_equipmentmodel_2.address = 'GPIB0::14::INSTR'
    instrumentation_equipmentmodel_2 = importer.save_or_locate(instrumentation_equipmentmodel_2)

    instrumentation_equipmentmodel_3 = EquipmentModel()
    instrumentation_equipmentmodel_3.distinguished_name = 'yaesu'
    instrumentation_equipmentmodel_3.display_name = 'Yaesu'
    instrumentation_equipmentmodel_3.description = 'Yaesu antenna forgató.'
    instrumentation_equipmentmodel_3.schema = instrumentation_schemamodel_2
    instrumentation_equipmentmodel_3._configuration = '{}'
    instrumentation_equipmentmodel_3.address = 'GPIB0::14::INSTR'
    instrumentation_equipmentmodel_3 = importer.save_or_locate(instrumentation_equipmentmodel_3)

    instrumentation_equipmentmodel_4 = EquipmentModel()
    instrumentation_equipmentmodel_4.distinguished_name = 'hp8591e'
    instrumentation_equipmentmodel_4.display_name = 'HP-8591E'
    instrumentation_equipmentmodel_4.description = 'HP-8591E spektrum analizátor.'
    instrumentation_equipmentmodel_4.schema = instrumentation_schemamodel_3
    instrumentation_equipmentmodel_4._configuration = '{}'
    instrumentation_equipmentmodel_4.address = 'GPIB0::14::INSTR'
    instrumentation_equipmentmodel_4 = importer.save_or_locate(instrumentation_equipmentmodel_4)

    instrumentation_equipmentmodel_5 = EquipmentModel()
    instrumentation_equipmentmodel_5.distinguished_name = 'narda'
    instrumentation_equipmentmodel_5.display_name = 'Narda RX-3000'
    instrumentation_equipmentmodel_5.description = 'Narda RX-3000 spektrum analizátor.'
    instrumentation_equipmentmodel_5.schema = instrumentation_schemamodel_3
    instrumentation_equipmentmodel_5._configuration = '{}'
    instrumentation_equipmentmodel_5.address = 'GPIB0::14::INSTR'
    instrumentation_equipmentmodel_5 = importer.save_or_locate(instrumentation_equipmentmodel_5)
