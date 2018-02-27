import numbers
import string
from more_itertools import peekable

# Raised if literally anything goes wrong
class ParseError(Exception):
    pass


# JSON syntactic elements
_object_start = '{'
_object_end = '}'

_array_start = '['
_array_end = ']'

_string_delimiter = '"'
_numeric_start = ('-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
_boolean_start = ('t', 'f')
_null_start = 'n'

_token_separator = ','
_pair_separator = ':'

def _whitespace_skip(json_iterator : peekable):
    while json_iterator.peek() in string.whitespace:
        json_iterator.next()

def _parse_string(json_iterator : peekable) -> str:
    result = ''
    json_iterator.next() # Skip over opening "

    while True:
        next_char = json_iterator.next()
        if next_char == '"' and not result.endswith('\\'):
            break
        result += next_char

    return result

def _parse_numeric(json_iterator : peekable) -> numbers.Number:
    value = ''

    next_char = json_iterator.next()
    while True:
        value += next_char
        next_char = json_iterator.peek()
        if next_char in string.whitespace or next_char in (_token_separator, _object_end, _array_end):
            break
        else:
            next_char = json_iterator.next()

    try:
        return int(value)
    except ValueError:
        return float(value)

def _parse_boolean(json_iterator : peekable) -> bool:
    value = ''
    
    next_char = json_iterator.next()
    
    while next_char not in string.whitespace and next_char not in (_token_separator, _object_end, _array_end):
        value += next_char
        next_char = json_iterator.next()

    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        raise ParseError('Invalid string "' + value + '" found while trying to parse a boolean value')

def _parse_null(json_iterator : peekable):
    value = ''
        
    next_char = json_iterator.next()
    while next_char not in string.whitespace and next_char not in (_token_separator, _object_end, _array_end):
        value += next_char
        next_char = json_iterator.next()

    if value == 'null':
        return None
    else:
        raise ParseError('Invalid string "' + value + '" found while trying to parse a null value')

def _parse_array(json_iterator : peekable) -> list:
    values = []    
    json_iterator.next() # Skip over opening [
    _whitespace_skip(json_iterator)
    next_char = json_iterator.peek()
    
    if next_char == _array_end:
        return [] # Empty Array

    while True:
        if next_char == _object_start:
            element_value = _parse_object(json_iterator)
        elif next_char == _array_start:
            element_value = _parse_array(json_iterator)
        elif next_char == _string_delimiter:
            element_value = _parse_string(json_iterator)
        elif next_char in _numeric_start:
            element_value = _parse_numeric(json_iterator)
        elif next_char in _boolean_start: # JSON defines boolean values as "true" or "false" exclusively
            element_value = _parse_boolean(json_iterator)
        elif next_char == _null_start: # JSON defines a "null" value
            element_value = _parse_null(json_iterator)

        values.append(element_value)

        _whitespace_skip(json_iterator)
        next_char = json_iterator.peek()
        if next_char == _array_end:
            json_iterator.next()
            return values
        elif next_char == _token_separator:
            next_char = json_iterator.next()
            _whitespace_skip(json_iterator)
            next_char = json_iterator.peek()
        else:
            raise ParseError('Unexpected character while trying to parse array: "' + next_char + '"')


def _parse_object(json_iterator : peekable) -> dict:
    next_char = json_iterator.next()
    if next_char != _object_start:
        raise ParseError('Unexpected character while trying to parse object: "' + next_char + '"')

    # Skip over whitespace
    _whitespace_skip(json_iterator)

    next_char = json_iterator.peek()

    if next_char == _object_end:
        return {}

    tokens = {}

    while True:
        # At the object level, a valid element follows the form "<element name AS string> : <value>"
        if json_iterator.peek() not in (_string_delimiter, _token_separator):
            raise ParseError('Unexpected character: "' + next_char + '"')
        element_name = _parse_string(json_iterator)
        element_value = None
        
        # Advance to the separator and the start of the value
        _whitespace_skip(json_iterator)
        next_char = json_iterator.peek()
        if next_char != _pair_separator:
            raise ParseError('Unexpected character while parsing element ' + element_name + ': "' + next_char + '"')
        json_iterator.next()
        _whitespace_skip(json_iterator)

        # Parse the value element
        next_char = json_iterator.peek()
        if next_char == _object_start:
            element_value = _parse_object(json_iterator)
        elif next_char == _array_start:
            element_value = _parse_array(json_iterator)
        elif next_char == _string_delimiter:
            element_value = _parse_string(json_iterator)
        elif next_char in _numeric_start:
            element_value = _parse_numeric(json_iterator)
        elif next_char in _boolean_start: # JSON defines boolean values as "true" or "false" exclusively
            element_value = _parse_boolean(json_iterator)
        elif next_char == _null_start: # JSON defines a "null" value
            element_value = _parse_null(json_iterator)
        else: # We've hit something invalid, let's abort
            raise ParseError('Unexpected character while parsing element ' + element_name + ': "' + next_char + '"')

        tokens[element_name] = element_value

        # Advance the iterator over whitespace, the token separator, whitespace to the start of the next token
        _whitespace_skip(json_iterator)
        next_char = json_iterator.peek()
        if not next_char in (_pair_separator, _object_end, _token_separator):
            raise ParseError('Unexpected character while parsing element ' + element_name + ': "' + next_char + '"')
        json_iterator.next()
        if next_char == _object_end:
            break
        _whitespace_skip(json_iterator)

    return tokens
    
# Check if the number of opening and closing elements for objects and arrays match up
# returns true if they do, if they don't, the returned list of strings will indicate which test(s) failed
def _syntax_check(json : str) -> (bool, list):
    check_content = json != ''
    check_objects = json.count(_object_start) - json.count(_object_end) == 0
    check_arrays = json.count(_array_start) - json.count(_array_end) == 0

    if check_objects and check_arrays and check_content:
        return (True, [])
    else:
        fails = []
        if not check_objects:
            fails.append('objects')
        if not check_arrays:
            fails.append('arrays')
        if not check_content:
            fails.append('empty string')
        return (False, fails)

# Given a json string, return a representation of that string as a dict 
def json_parse(json : str) -> dict:
    (success, failures) = _syntax_check(json)
    if not success:
        raise ParseError('Passed string is not valid json. Could not validate the following elements: ' + repr(failures))

    return _parse_object(peekable(json))