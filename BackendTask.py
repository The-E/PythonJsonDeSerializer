

class PropertySet(object):

    def __init__(self, name, *args, **kwargs):
        super(PropertySet, self).__init__(*args, **kwargs)

        self.type = 'PropertySet'
        self.name = name
        self.properties = []

class Property(object):

    def __init__(self, name, value, *args, **kwargs):
        super(Property, self).__init__(*args, **kwargs)

        self.type = 'Property'
        self.name = name
        self.value = value