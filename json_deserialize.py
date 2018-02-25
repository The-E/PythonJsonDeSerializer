from typing import *
from types import *
from BackendTask import * 

def tokenize(json : str):
    data = json
    result = {}

    tmp = data.partition(':')

    while tmp[2] != '':
        key = tmp[0].rstrip(' ,"').lstrip(' ,"')
        value = tmp[2].rstrip().lstrip()
    
        if value.startswith('['):
            value = value.split(']', 1)
        elif value.startswith('{'):
            value = value.split('}', 1)
        else:
            value = value.split(',', 1)

        result[key] = value[0]
        if len(value) > 1: 
            tmp = value[1].partition(':')
        else:
            break # we've reached the end of the input string

    return result

def parse_simple(json : str):
    raw = json.lstrip().rstrip()
    if raw.startswith('"'): #handle as string; strip enclosing ""
        return raw.lstrip(' "').rstrip(' "')
    else: #numeric type
        try:
            return int(raw)
        except ValueError:
            return float(raw)

def parse_collection(json : str):
    raw = json.lstrip(' [').rstrip(' ]')
    items = raw.split('}')

    result = []

    for item_string in items:
        if item_string == '':
            continue
        item = {}
        item_string.lstrip(' ,{')
        subitems = item_string.split(',')
        for subitem_string in subitems:
            if subitem_string == '': 
                continue
            kvp = subitem_string.split(':')
            key = kvp[0].lstrip(' ,{"').rstrip(' "')
            value = parse_simple(kvp[1])
            item[key] = value

        result.append(item)
    
    return result

def get_value(json):
    if not json.startswith(('{', '[')):
        return parse_simple(json)
    else:
        return parse_collection(json)

def json_deserialize(json : str):
    if not json.startswith('{') or not json.endswith('}'):
        raise TypeError('Input is not a valid JSON object')

    result = {}

    parseable = json.lstrip(' {').rstrip('} ')
    tokens = tokenize(parseable)

    for key in tokens.keys():
        result[key.lstrip(' "').rstrip(' "')] = get_value(tokens[key])

    return result

def property_set_deserialize(json) -> PropertySet:
    parsed_object = json_deserialize(json)

    # Is this a PropertySet?
    if 'type' not in parsed_object:
        raise SyntaxError('Could not find type string')

    if 'name' not in parsed_object:
        raise SyntaxError('Could not find name string')

    if not parsed_object['type'] == 'PropertySet':
        raise SyntaxError('PropertySet invalid: Type string is: ' + parsed_object['type'] + ', should be "PropertySet"')

    property_set = PropertySet(parsed_object['name'])

    if 'properties' in parsed_object:
        for property in parsed_object['properties']:
            # Is this a property?
            if 'type' not in property:
                raise SyntaxError('Property invalid: No type string found')
            if not property['type'] == 'Property':
                raise SyntaxError('Property invalid: Type string is ' + property['type'] + ', should be "Property"')
            if 'name' not in property:
                raise SyntaxError('Property invalid: No name string found')
            if 'value' not in property:
                raise SyntaxError('Property ' + property['name'] + ' is invalid: No value found')
            
            property_set.properties.append(Property(property['name'], property['value']))
    
    return property_set