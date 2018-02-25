import unittest

from BackendTask import PropertySet
from BackendTask import Property
from json_serialize import json_serialize
from json_deserialize import *
from example_input import *

class Test_test_BackendTask(unittest.TestCase):

    def test_propertyset_create(self):

        a_property_set = PropertySet('Test')

        self.assertEquals(a_property_set.type, 'PropertySet')
        self.assertEquals(a_property_set.name, 'Test')
        self.assertTrue(len(a_property_set.properties) == 0)

    def test_property_create(self):

        a_property = Property('Test', 100)

        self.assertEquals(a_property.type, 'Property')
        self.assertEquals(a_property.name, 'Test')
        self.assertEquals(a_property.value, 100)

    def test_propertyset_serialize(self):
        self.maxDiff = None
        property_set = PropertySet('Test Property Set 1')
        property_set.properties.append(Property('Width', 100))
        property_set.properties.append(Property('Height', 100))
        property_set.properties.append(Property('ThermalTransmittance', 0.9))
        property_set.properties.append(Property('FireResistance', 'Class 4'))
        property_set.properties.append(Property('WindLoadRating', 'Class 3'))

        json = json_serialize(property_set)
        self.assertEquals(json, '{"name": "Test Property Set 1", "properties": [{"name": "Width", "type": "Property", "value": 100}, {"name": "Height", "type": "Property", "value": 100}, {"name": "ThermalTransmittance", "type": "Property", "value": 0.9}, {"name": "FireResistance", "type": "Property", "value": "Class 4"}, {"name": "WindLoadRating", "type": "Property", "value": "Class 3"}], "type": "PropertySet"}')
        
    def test_propertyset_deserialize(self):
        self.assertIsInstance(property_set_deserialize(example_input[0]), PropertySet)
        self.assertRaisesRegex(ParseError, 'Property invalid: No type string found', property_set_deserialize, example_input[1])
        self.assertRaisesRegex(ParseError, 'Property WindLoadRating is invalid: No value found', property_set_deserialize, example_input[2])
        self.assertRaisesRegex(ParseError, 'Property invalid: No name string found', property_set_deserialize, example_input[3])
        self.assertRaisesRegex(ParseError, 'Property invalid: Type string is Properti, should be "Property"', property_set_deserialize, example_input[4])
        self.assertRaisesRegex(ParseError, 'PropertySet invalid: Type string is: PropertiSet, should be "PropertySet"', property_set_deserialize, example_input[5])

    def test_serialization_loop(self):
        property_set = PropertySet('Test Property Set 1')
        property_set.properties.append(Property('Width', 100))
        property_set.properties.append(Property('Height', 100))
        property_set.properties.append(Property('ThermalTransmittance', 0.9))
        property_set.properties.append(Property('FireResistance', 'Class 4'))
        property_set.properties.append(Property('WindLoadRating', 'Class 3'))

        json = json_serialize(property_set)
        self.assertIsInstance(property_set_deserialize(json), PropertySet)

if __name__ == '__main__':
    unittest.main()
