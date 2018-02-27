import io

# Helper functions
def _is_builtin_class_instance(obj):
    return obj.__class__.__module__ == 'builtins'

# Marks the last element of a collection 
def islast(o):
    it = iter(o)
    e = next(it)
    while True:
        try:
            nxt = next(it)
            yield (False, e)
            e = nxt
        except StopIteration:
            yield (True, e)
            break

def _collection_serialize(obj):
    result = io.StringIO()

    result.write('[')
    for (last, value) in islast(obj):
        if _is_builtin_class_instance(value):
            if isinstance(value, str):
                result.write('\"' + value + '\"')
            else:
                if value == None:
                    result.write('null')
                else:
                    result.write(repr(value).lower())
        else:
            result.write(json_serialize(value))
        if not last:
            result.write(', ')
    result.write(']')

    return result.getvalue()

def _dict_serialize(obj : dict):
    if len(obj.keys()) == 0:
        return '{}'
    
    result = io.StringIO()

    result.write('{')

    for key in obj:
        result.write('"' + key + '" : ' )
        value = obj[key]
        if isinstance(value, (list, tuple)):
            result.write(_collection_serialize(value))
        elif isinstance(value, dict):
            result.write(_dict_serialize(value))
        else:
            if (_is_builtin_class_instance(value)):
                if isinstance(value, str):
                    result.write('\"' + value + '\"')
                else:
                    if value == None:
                        result.write('null')
                    else:
                        result.write(repr(value).lower())
            else:
                result.write(json_serialize(value))
        result.write(',')

    output = result.getvalue()[:-1]
    output += '}'

    return output

def json_serialize(obj):
    result = io.StringIO()

    if isinstance(obj, (list, tuple)):
        return _collection_serialize(obj)
    if isinstance(obj, dict):
        return _dict_serialize(obj)

    result.write('{')

    properties = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]

    for (last, property) in islast(properties):
        result.write('\"' + property + '\": ')
        value = getattr(obj, property)
        if isinstance(value, (list, tuple)):
            result.write(_collection_serialize(value))
        elif isinstance(value, dict):
            result.write(_dict_serialize)
        else:
            if (_is_builtin_class_instance(value)):
                if isinstance(value, str):
                    result.write('\"' + value + '\"')
                else:
                    if value == None:
                        result.write('null')
                    else:
                        result.write(repr(value).lower())
            else:
                result.write(json_serialize(value))
        if not last:
            result.write(', ')
    
    result.write('}')

    return result.getvalue()