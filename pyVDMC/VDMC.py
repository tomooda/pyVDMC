from types import MethodType

import requests
import json

DEFAULT_SERVER = "http://vdmpad.csce.kyushu-u.ac.jp/"
#DEFAULT_SERVER = "http://localhost:8085/"

class VDMError(Exception):
    pass

class TestFailed(Exception):
    def __init__(self, msg, expected, actual):
        Exception(self, msg)
        this.expected = expected
        this.actual = actual

class VDMC:
    """
    VDMPad client
    """
    def __init__(self, source=str(), states=dict(), server = DEFAULT_SERVER):
        if server[-1] != '/':
            server += "/"
        self.url = server+"eval"
        self.source = source
        self.states = states
    def eval(self, expr):
        data = self.states.copy()
        data['source'] = self.source
        data['expression'] = expr
        response = requests.post(self.url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        result = response.json()
        if result['message']:
            raise VDMError(result['message'])
        poststates = dict()
        for key in result:
            if '`' in key:
                poststates[key] = result[key]
        self.states = poststates
        return result['value']
    __call__ = eval

def vdm_module(*states):
    def _vdm_module(klass):
        spec = klass.__doc__
        vdm = VDMC(spec)
        def __to_vdm(self):
            for var in states:
                vdm.states['DEFAULT`'+var] = str(getattr(self, var))
        def __eval_vdm(self, method, *args):
            return eval(vdm(method.__name__ + '('+','.join([str(arg) for arg in args])+')'))
        def __from_vdm(self):
            for var in states:
                setattr(self, var, eval(vdm.states['DEFAULT`'+var]))
        def __test_vdm(self):
            for var in states:
                expected = eval(vdm.states['DEFAULT`'+var])
                actual = getattr(self, var)
                if actual != expected:
                    raise TestFailure("%s Expected: %s Actual %s"%(var, expected, actual), expected, actual)

        klass.__to_vdm = MethodType(__to_vdm, None, klass)
        klass.__eval_vdm = MethodType(__eval_vdm, None, klass)
        klass.__from_vdm = MethodType(__from_vdm, None, klass)
        klass.__test_vdm = MethodType(__from_vdm, None, klass)
        return klass
    return _vdm_module

def vdm_method(method):
    def __eval(self, *args):
        self.__to_vdm()
        RESULT = self.__eval_vdm(method, *args)
        self.__from_vdm()
        return RESULT
    return __eval

def vdm_test(method):
    def __test(self, *args):
        self.__to_vdm()
        RESULT = self.__eval_vdm(method, *args)
        result = method(self, *args)
        if result != RESULT:
            raise TestFailed("Expected: %s Actual: %s"%(RESULT, result), RESULT, result)
        self.__test_vdm()
        return result
    return __test
