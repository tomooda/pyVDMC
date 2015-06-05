from __future__ import absolute_import
import json
from .VDMValue import *

class VDMWriter:
    def __init__(self):
        self.specials = dict()
    def stringify(self, obj):
        className = obj.__class__.__name__
        if className in self.specials:
            return self.specials[className](self, obj)
        if isinstance(obj, int) or isinstance(obj, float):
            return str(obj)
        if obj is None:
            return str("nil")
        if obj is True:
            return str("true")
        if obj is False:
            return str("false")
        if isinstance(obj, str):
            return json.dumps(obj)
        if isinstance(obj, Quote):
            return str(obj)
        if isinstance(obj, Composite):
            return "mk_"+obj.typeName+"("+",".join((self.stringify(arg) for arg in obj))+")"
        if isinstance(obj, Token):
            return "mk_token("+self.stringify(obj.value)+")"
        if isinstance(obj, tuple):
            return "mk_("+",".join((self.stringify(arg) for arg in obj))+")"
        if isinstance(obj, list):
            return "["+",".join((self.stringify(arg) for arg in obj))+"]"
        if isinstance(obj, set):
            return "{"+",".join((self.stringify(arg) for arg in obj))+"}"
        if isinstance(obj, dict):
            if obj:
                return "{"+",".join((self.stringify(k)+"|->"+self.stringify(v) for k,v in obj.items()))+"}"
            else:
                return "{|->}"
        try:
            return "mk_"+obj.__class__.__name__+"("+",".join((self.stringify(arg) for arg in obj))+")"
        except AttributeError:
            return "mk_"+obj.__class__.__name__+"()"
    __call__ = stringify
