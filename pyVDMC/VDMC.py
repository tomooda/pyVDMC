import requests
import json

class VDMError(Exception):
    pass

class VDMC:
    """
    VDMPad client
    """
    def __init__(self, source=str(), states=dict(), server = "http://vdmpad.csce.kyushu-u.ac.jp/"):
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
