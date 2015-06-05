class Composite:
    """
    The Composite class is a container object for VDM's composite type.
    The repr method returns a python expression to construct the value, and
    the str method returns a VDM expression to construct the value.
    The members can be accessed by integer indices.
    """
    def __init__(self, typeName, *args):
        self.typeName = typeName
        self.args = tuple(args)

    def __len__(self):
        return len(self.args)
    def __getitem__(self, index):
        return self.args[index]
    def __iter__(self):
        return iter(self.args)
    def __eq__(self, obj):
        return self.__class__ == obj.__class__ and self.typeName == obj.typeName and self.args == obj.args
    def __lt__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("unorderable types: %s() < %s()" %(self.__class__.__name__, obj.__class__.__name__))
        if self.typeName < obj.typeName:
            return True
        if self.typeName != obj.typeName:
            return False
        return self.args < obj.args
    def __le__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("unorderable types: %s() < %s()" %(self.__class__.__name__, obj.__class__.__name__))
        if self.typeName < obj.typeName:
            return True
        if self.typeName != obj.typeName:
            return False
        return self.args <= obj.args
    def __cmp__(self, obj):
        c = cmp(self.__class__, obj.__class__)
        if c:
            return c
        c = cmp(self.typeName, obj.typeName)
        if c:
            return c
        return cmp(self.args, obj.args)
    def __hash__(self):
        return hash(self.typeName) * 1024 + hash(self.args)
        
    def __str__(self):
        return "mk_"+self.typeName+"("+",".join((_printArg(arg) for arg in self.args))+")"
    def __repr__(self):
        return self.__class__.__name__+"("+",".join((repr(arg) for arg in [self.typeName]+list(self.args)))+")"
        
class Quote:
    """
    The Quote class is a container object for VDM's quote type.
    The repr method returns a python expression to construct the value, and
    the str method returns a VDM expression to construct the value.
    """
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Quote type must be given a string parameter")
        self.name = name

    def __eq__(self, obj):
        return self.__class__ == obj.__class__ and self.name == obj.name
    def __lt__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("unorderable types: %s() < %s()" %(self.__class__.__name__, obj.__class__.__name__))
        return self.name < obj.name
    def __le__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("unorderable types: %s() < %s()" %(self.__class__.__name__, obj.__class__.__name__))
        return self.name <= obj.name
    def __cmp__(self, obj):
        c = cmp(self.__class__, obj.__class__)
        if c:
            return c
        return cmp(self.name, obj.name)
    def __hash__(self):
        return hash(self.name) ^ hash(self.__class__)
        
    def __str__(self):
        return "<"+self.name+">"
    def __repr__(self):
        return self.__class__.__name__+"("+self.name+")"
    
class Token:
    """
    The Token class is a container object for VDM's token type.
    The repr method returns a python expression to construct the value, and
    the str method returns a VDM expression to construct the value.
    """
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Quote type must be given a string parameter")
        self.value = value

    def __eq__(self, obj):
        return self.__class__ == obj.__class__ and self.value == obj.value
    def __lt__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("unorderable types: %s() < %s()" %(self.__class__.__name__, obj.__class__.__name__))
        return self.value < obj.value
    def __le__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError("unorderable types: %s() < %s()" %(self.__class__.__name__, obj.__class__.__name__))
        return self.value <= obj.value
    def __cmp__(self, obj):
        c = cmp(self.__class__, obj.__class__)
        if c:
            return c
        return cmp(self.value, obj.value)
    def __hash__(self):
        return hash(self.value) ^ hash(self.__class__)
        
    def __str__(self):
        return "mk_token("+_printArg(self.value)+")"
    def __repr__(self):
        return self.__class__.__name__+"("+repr(self.value)+")"
    

def _printArg(arg):
    if arg is True:
        return 'true'
    if arg is False:
        return 'false'
    if arg is None:
        return 'nil'
    if isinstance(arg, str):
        return repr(arg)
    return str(arg)

VDM_TRUE = 0
VDM_FALSE = 1
VDM_NUM = 2
VDM_CHAR = 3
VDM_QUOTE = 4
VDM_TOKEN = 5
VDM_SET = 10
VDM_SEQ = 11
VDM_MAP = 12
VDM_TUPLE = 13
VDM_COMPOSITE = 14
VDM_NIL = 15
VDM_STRING = 16
