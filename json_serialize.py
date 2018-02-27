import io

# Helper functions
def is_builtin_class_instance(obj):
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

def collection_serialize(obj):
    result = io.StringIO()

    result.write('[')
    for (last, value) in islast(obj):
        if is_builtin_class_instance(value):
            if isinstance(value, str):
                result.write('\"' + value + '\"')
            else:
                result.write(repr(value))
        else:
            result.write(json_serialize(value))
        if not last:
            result.write(', ')
    result.write(']')

    return result.getvalue()

def json_serialize(obj):
    result = io.StringIO()

    if isinstance(obj, (list, tuple)):
        return collection_serialize(obj)

    result.write('{')

    properties = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]

    for (last, property) in islast(properties):
        result.write('\"' + property + '\": ')
        value = getattr(obj, property)
        if isinstance(value, (list, tuple)):
            result.write(collection_serialize(value))
        else:
            if (is_builtin_class_instance(value)):
                if isinstance(value, str):
                    result.write('\"' + value + '\"')
                else:
                    result.write(repr(value))
            else:
                result.write(json_serialize(value))
        if not last:
            result.write(', ')
    
    result.write('}')

    return result.getvalue()