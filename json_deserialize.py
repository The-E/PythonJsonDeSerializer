from BackendTask import *
from json_parse import json_parse

def property_set_deserialize(json) -> PropertySet:
    parsed_object = json_parse(json)

    # Is this a PropertySet?
    if 'name' not in parsed_object:
        raise ParseError('PropertySet invalid: Could not find name string')

    if 'type' not in parsed_object:
        raise ParseError('PropertySet ' + parsed_object['name'] + ' is invalid: Could not find type string')

    if not parsed_object['type'] == 'PropertySet':
        raise ParseError('PropertySet ' + parsed_object['name'] + ' is invalid: Type string is: ' + parsed_object['type'] + ', should be "PropertySet"')

    property_set = PropertySet(parsed_object['name'])

    if 'properties' in parsed_object:
        for property in parsed_object['properties']:
            # Is this a property?
            if 'name' not in property:
                raise ParseError('Property is invalid: No name string found')
            if 'type' not in property:
                raise ParseError('Property ' + property['name'] + ' is invalid: No type string found')
            if not property['type'] == 'Property':
                raise ParseError('Property ' + property['name'] + ' is invalid: Type string is ' + property['type'] + ', should be "Property"')          
            if 'value' not in property:
                raise ParseError('Property ' + property['name'] + ' is invalid: No value found')
            
            property_set.properties.append(Property(property['name'], property['value']))
    
    return property_set

class ParseError(Exception):
    pass