import unittest
import json_parser
import json_serializer
import property_set_deserializer

from BackendTask import PropertySet
from BackendTask import Property
from example_input import *

class Test_test_BackendTask(unittest.TestCase):

    def test_propertyset_create(self):

        a_property_set = PropertySet('Test')

        self.assertEqual(a_property_set.type, 'PropertySet')
        self.assertEqual(a_property_set.name, 'Test')
        self.assertTrue(len(a_property_set.properties) == 0)

    def test_property_create(self):

        a_property = Property('Test', 100)

        self.assertEqual(a_property.type, 'Property')
        self.assertEqual(a_property.name, 'Test')
        self.assertEqual(a_property.value, 100)

    def test_propertyset_serialize(self):
        self.maxDiff = None
        property_set = PropertySet('Test Property Set 1')
        property_set.properties.append(Property('Width', 100))
        property_set.properties.append(Property('Height', 100))
        property_set.properties.append(Property('ThermalTransmittance', 0.9))
        property_set.properties.append(Property('FireResistance', 'Class 4'))
        property_set.properties.append(Property('WindLoadRating', 'Class 3'))

        json = json_serializer.json_serialize(property_set)
        self.assertEqual(json, '{"name": "Test Property Set 1", "properties": [{"name": "Width", "type": "Property", "value": 100}, {"name": "Height", "type": "Property", "value": 100}, {"name": "ThermalTransmittance", "type": "Property", "value": 0.9}, {"name": "FireResistance", "type": "Property", "value": "Class 4"}, {"name": "WindLoadRating", "type": "Property", "value": "Class 3"}], "type": "PropertySet"}')
        
    def test_propertyset_deserialize(self):
        property_set = property_set_deserializer.property_set_deserialize(example_input[0])
        self.assertIsInstance(property_set, PropertySet)
        self.assertEqual(property_set.name, 'A Property Set 1')
        self.assertEqual(property_set.type, 'PropertySet')
        self.assertEqual(len(property_set.properties), 5)
        self.assertEqual(property_set.properties[0].name,  'Width')
        self.assertEqual(property_set.properties[0].value,  100)
        self.assertEqual(property_set.properties[0].type,  'Property')
        self.assertEqual(property_set.properties[1].name,  'Height')
        self.assertEqual(property_set.properties[1].value,  100)
        self.assertEqual(property_set.properties[1].type,  'Property')
        self.assertEqual(property_set.properties[2].name,  'ThermalTransmittance')
        self.assertEqual(property_set.properties[2].value,  0.9)
        self.assertEqual(property_set.properties[2].type,  'Property')
        self.assertEqual(property_set.properties[3].name,  'FireResistance')
        self.assertEqual(property_set.properties[3].value, 'Class 4')
        self.assertEqual(property_set.properties[3].type,  'Property')
        self.assertEqual(property_set.properties[4].name,  'WindLoadRating')
        self.assertEqual(property_set.properties[4].value, 'Class 3')
        self.assertEqual(property_set.properties[4].type,  'Property')
        
        self.assertRaisesRegex(property_set_deserializer.ParseError, 'Property ThermalTransmittance is invalid: No type string found', property_set_deserializer.property_set_deserialize, example_input[1])
        self.assertRaisesRegex(property_set_deserializer.ParseError, 'Property WindLoadRating is invalid: No value found', property_set_deserializer.property_set_deserialize, example_input[2])
        self.assertRaisesRegex(property_set_deserializer.ParseError, 'Property is invalid: No name string found', property_set_deserializer.property_set_deserialize, example_input[3])
        self.assertRaisesRegex(property_set_deserializer.ParseError, 'Property FireResistance is invalid: Type string is Properti, should be "Property"', property_set_deserializer.property_set_deserialize, example_input[4])
        self.assertRaisesRegex(property_set_deserializer.ParseError, 'PropertySet A Property Set 6 is invalid: Type string is: PropertiSet, should be "PropertySet"', property_set_deserializer.property_set_deserialize, example_input[5])

    def test_serialization_loop(self):
        property_set = PropertySet('Test Property Set 1')
        property_set.properties.append(Property('Width', 100))
        property_set.properties.append(Property('Height', 100))
        property_set.properties.append(Property('ThermalTransmittance', 0.9))
        property_set.properties.append(Property('FireResistance', 'Class 4'))
        property_set.properties.append(Property('WindLoadRating', 'Class 3'))

        json = json_serializer.json_serialize(property_set)
        property_set_copy = property_set_deserializer.property_set_deserialize(json)

        self.assertIsInstance(property_set_copy, PropertySet)
        self.assertEqual(property_set.name, property_set_copy.name)
        self.assertEqual(property_set.type, property_set_copy.type)
        self.assertEqual(len(property_set.properties), len(property_set_copy.properties))
        self.assertEqual(property_set.properties[0].name,  property_set_copy.properties[0].name) 
        self.assertEqual(property_set.properties[0].value, property_set_copy.properties[0].value)
        self.assertEqual(property_set.properties[0].type,  property_set_copy.properties[0].type) 
        self.assertEqual(property_set.properties[1].name,  property_set_copy.properties[1].name) 
        self.assertEqual(property_set.properties[1].value, property_set_copy.properties[1].value)
        self.assertEqual(property_set.properties[1].type,  property_set_copy.properties[1].type) 
        self.assertEqual(property_set.properties[2].name,  property_set_copy.properties[2].name) 
        self.assertEqual(property_set.properties[2].value, property_set_copy.properties[2].value)
        self.assertEqual(property_set.properties[2].type,  property_set_copy.properties[2].type) 
        self.assertEqual(property_set.properties[3].name,  property_set_copy.properties[3].name) 
        self.assertEqual(property_set.properties[3].value, property_set_copy.properties[3].value)
        self.assertEqual(property_set.properties[3].type,  property_set_copy.properties[3].type) 
        self.assertEqual(property_set.properties[4].name,  property_set_copy.properties[4].name) 
        self.assertEqual(property_set.properties[4].value, property_set_copy.properties[4].value)
        self.assertEqual(property_set.properties[4].type,  property_set_copy.properties[4].type) 

    def test_json(self):
        self.assertEqual(json_parser.json_parse('{}'), {})
        self.assertRaises(json_parser.ParseError, json_parser.json_parse, '')
        self.assertRaises(json_parser.ParseError, json_parser.json_parse, '[]')
        self.assertRaises(json_parser.ParseError, json_parser.json_parse, 'A string')
        self.assertRaises(json_parser.ParseError, json_parser.json_parse, '{"name": "Test Property Set 1", "properties": [{"name": "Width", "type":')
        self.assertRaises(json_parser.ParseError, json_parser.json_parse, '{ asdvhbawlrga }')
        self.assertRaises(json_parser.ParseError, json_parser.json_parse, '{ "name" : nope }')

if __name__ == '__main__':
    unittest.main()
