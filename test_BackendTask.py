import unittest

from BackendTask import PropertySet
from BackendTask import Property

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

if __name__ == '__main__':
    unittest.main()
