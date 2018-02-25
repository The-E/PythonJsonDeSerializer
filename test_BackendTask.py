import unittest

from BackendTask import PropertySet
from BackendTask import Property
from json_serialize import *
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

    #def test_propertyset_serialize(self):
    #    property_set = PropertySet('Test Property Set 1')
    #    property_set.properties.append(Property('Width', 100))
    #    property_set.properties.append(Property('Height', 100))
    #    property_set.properties.append(Property('ThermalTransmittance', 0.9))
    #    property_set.properties.append(Property('FireResistance', 'Class 4'))
    #    property_set.properties.append(Property('WindLoadRating', 'Class 3'))

    #    json = json_serialize(property_set)

    #    self.assertEquals(json, example_input[0])
        
    def test_propertyset_deserialize(self):
        property_set_0 = property_set_deserialize(example_input[0])
        self.assertRaisesRegex(SyntaxError, 'Property invalid: No type string found', property_set_deserialize, example_input[1])
        self.assertRaisesRegex(SyntaxError, 'Property WindLoadRating is invalid: No value found', property_set_deserialize, example_input[2])
        self.assertRaisesRegex(SyntaxError, 'Property invalid: No name string found', property_set_deserialize, example_input[3])
        self.assertRaisesRegex(SyntaxError, 'Property invalid: Type string is Properti, should be "Property"', property_set_deserialize, example_input[4])
        self.assertRaisesRegex(SyntaxError, 'Type string is: PropertiSet, should be "PropertySet"', property_set_deserialize, example_input[5])


if __name__ == '__main__':
    unittest.main()
