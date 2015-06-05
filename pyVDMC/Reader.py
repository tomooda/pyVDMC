from __future__ import absolute_import
from math import *
from .VDMValue import *

class VDMReader:
    def __init__(self):
        self.specials = dict()
    def parse(self, string):
        return self._parse(_Stream(string))
    def _parse(self, source):
        source.skipSeparators()
        char = source.peek()
        if char == 'n':
            return self._parseNil(source)
        elif char == 't':
            return self._parseTrue(source)
        elif char == 'f':
            return self._parseFalse(source)
        elif char == 'm':
            return self._parseComposite(source)
        elif char == '{':
            return self._parseSetOrMap(source)
        elif char == '[':
            return self._parseSeq(source)
        elif char == '<':
            return self._parseQuote(source)
        elif char == "'":
            return self._parseChar(source)
        elif char == '"':
            return self._parseString(source)
        elif char == '-' or char.isdigit():
            return self._parseNumber(source)
        else:
            raise VDMSyntaxError("A value expected here:"+source.next(10))
    def _parseNil(self, source):
        if source.nextMatch("nil"):
            if VDM_NIL in self.specials:
                self.specials[VDM_NIL](self, "nil")
            return None
        raise VDMSyntaxError("A value expected here:"+source.next(10))
    def _parseTrue(self, source):
        if source.nextMatch("true"):
            if VDM_TRUE in self.specials:
                self.specials[VDM_NIL](self, "true")
            return True
        raise VDMSyntaxError("A value expected here:"+source.next(10))
    def _parseFalse(self, source):
        if source.nextMatch("false"):
            if VDM_FALSE in self.specials:
                self.specials[VDM_NIL](self, "false")
            return False
        raise VDMSyntaxError("A value expected here:"+source.next(10))
    def _parseComposite(self, source):
        if not source.nextMatch("mk_"):
            raise VDMSyntaxError("A value expected here:"+source.next(10))
        typeName = source.upto('(').strip()
        args = list()
        source.skipSeparators()
        if source.peek() != ')':
            while True:
                args.append(self._parse(source))
                source.skipSeparators()
                if source.peek() != ',':
                    break
                source.next()
        if not source.nextMatch(')'):
            raise VDMSyntaxError("A comma or ) expected here: "+source.next(10))
        if typeName == "":
            if len(args) < 2:
                raise VDMSyntaxError("A tuple must have more than one parameters: %s"%(args,))
            if VDM_TUPLE in self.specials:
                return self.specials[VDM_TUPLE](self, args)
            return tuple(args)
        if typeName == "token":
            if len(args) != 1:
                raise VDMSyntaxError("A token must have only one parameters: %s"%(args,))
            if VDM_TOKEN in self.specials:
                return self.specials[VDM_TOKEN](self, args[0])
            return Token(args[0])
        if typeName in self.specials:
            return self.specials[typeName](self, args)
        if VDM_COMPOSITE in self.specials:
            return self.specials[VDM_COMPOSITE](self, typeName, *args)
        return Composite(typeName, *args)
    def _parseSetOrMap(self, source):
        if not source.nextMatch('{'):
            raise VDMSyntaxError("Expected { : "+source.next(10))
        source.skipSeparators()
        if source.peek() == '}':
            source.next()
            if VDM_SET in self.specials:
                return self.specials[VDM_SET](self, list())
            return set()
        if source.peek() == '|':
            if not source.nextMatch('|->'):
                raise VDMSyntaxError("Expected |-> : "+source.next(10))
            source.skipSeparators()
            if not source.nextMatch('}'):
                raise VDMSyntaxError("Expected } : "+source.next(10))
            if VDM_MAP in self.specials:
                return self.specials[VDM_MAP](self, list())
            return dict()
        first = self._parse(source)
        source.skipSeparators()
        if source.peek() == '|':
            if not source.nextMatch("|->"):
                raise VDMSyntaxError("Expected |-> : "+source.next(10))
            value = self._parse(source)
            return self._parseMap(source, (first, value))
        return self._parseSet(source, first)
    def _parseMap(self, source, first):
        source.skipSeparators()
        items = list()
        items.append(first)
        while source.peek() == ',':
            source.next()
            key = self._parse(source)
            source.skipSeparators()
            if not source.nextMatch("|->"):
                raise VDMSyntaxError("Expected |-> : "+source.next(10))
            value = self._parse(source)
            items.append((key, value))
            source.skipSeparators()
        if not source.nextMatch('}'):
            raise VDMSyntaxError("Expected } : "+source.next(10))
        if VDM_MAP in self.specials:
            return self.specials[VDM_MAP](self, items)
        return dict(items)
    def _parseSet(self, source, first):
        source.skipSeparators()
        items = list()
        items.append(first)
        while source.peek() == ',':
            source.next()
            items.append(self._parse(source))
            source.skipSeparators()
        if not source.nextMatch('}'):
            raise VDMSyntaxError("Expected } : "+source.next(10))
        if VDM_SET in self.specials:
            return self.specials[VDM_SET](self, items)
        return set(items)
    def _parseSeq(self, source):
        if not source.nextMatch("["):
            raise VDMSyntaxError("A value expected here:"+source.next(10))
        args = list()
        source.skipSeparators()
        if source.peek() != ']':
            while True:
                args.append(self._parse(source))
                source.skipSeparators()
                if source.peek() != ',':
                    break
                source.next()
        if not source.nextMatch(']'):
            raise VDMSyntaxError("A comma or ] expected here: "+source.next(10))
        if VDM_SEQ in self.specials:
            return self.specials[VDM_SEQ](self, args)
        return args
    def _parseQuote(self, source):
        if not source.nextMatch('<'):
            raise VDMSyntaxError("A value expected here:"+source.next(10))
        name = source.upto('>')
        for c in name:
            if not (c.isalnum() or c == '_'):
                raise VDMSyntaxError("Invalid character in a quote: "+source.next(10))
        if VDM_QUOTE in self.specials:
            return self.specials[VDM_QUOTE](self, name)
        return Quote(name)
    def _parseChar(self, source):
        if not source.nextMatch("'"):
            raise VDMSyntaxError("A value expected here:"+source.next(10))
        char = self._readChar(source)
        if char is None:
            raise VDMSyntaxError("Unexpected end of expression in a character literal")
        if not source.nextMatch("'"):
            raise VDMSyntaxError("' expected here:"+source.next(10))
        return char
    def _parseString(self, source):
        if not source.nextMatch('"'):
            raise VDMSyntaxError("A value expected here:"+source.next(10))
        string = str()
        while source.peek() != '"':
            char = self._readChar(source)
            if char is None:
                raise VDMSyntaxError("Unexpected end of expression in a string literal")
            string += char
        if not source.nextMatch('"'):
            raise VDMSyntaxError('" expected here:'+source.next(10))
        return string
    def _parseNumber(self, source):
        if source.peek() is None:
            raise VDMSyntaxError("A value expected here:"+source.next(10))
        expr = str()
        if source.peek() == '-':
            expr += source.next()
        while source.peek() is not None and source.peek().isdigit():
            expr += source.next()
        if source.peek() == '.':
            expr += source.next()
            while source.peek() is not None and source.peek().isdigit():
                expr += source.next()
        if source.peek() == 'e' or source.peek() == 'E':
            expr += source.next()
            if source.peek() == '-':
                expr += source.next()
            while source.peek() is not None and source.peek().isdigit():
                expr += source.next()
        if not expr or (expr[0] == '-' and not expr[1:]):
            raise VDMSyntaxError("Unexpected end of expression in a number literal")
        if expr.isdigit() or (expr[0] == '-' and expr[1:].isdigit()):
            return int(expr)
        else:
            return float(expr)

    def _readChar(self, source):
        c = source.next()
        if c != '\\':
            return c
        c = source.next()
        if c == '\\':
            return '\\'
        if c == 'r':
            return '\r'
        if c == 'n':
            return '\n'
        if c == 't':
            return '\t'
        if c == 'f':
            return '\f'
        if c == 'e':
            return chr(14)
        if c == 'a':
            return chr(10)
        if c == 'x':
            if source.peek() is None:
                return None
            c1 = source.next().lower()
            if c1 not in _HEX:
                raise VDMSynatxError("A hex value is expected: "+c1+source.next(9))
            c1 = _HEX.index(c1)
            if source.peek() is None:
                return None
            c2 = source.next().lower()
            if c2 not in _HEX:
                raise VDMSynatxError("A hex value is expected: "+c2+source.next(9))
            c2 = _HEX.index(c2)
            return unichr(c1*16+c2)
        if c == 'u':
            if source.peek() is None:
                return None
            c1 = source.next().lower()
            if c1 not in _HEX:
                raise VDMSynatxError("A hex value is expected: "+c1+source.next(9))
            c1 = _HEX.index(c1)
            if source.peek() is None:
                return None
            c2 = source.next().lower()
            if c2 not in _HEX:
                raise VDMSynatxError("A hex value is expected: "+c2+source.next(9))
            c2 = _HEX.index(c2)
            if source.peek() is None:
                return None
            c3 = source.next().lower()
            if c3 not in _HEX:
                raise VDMSynatxError("A hex value is expected: "+c3+source.next(9))
            c3 = _HEX.index(c3)
            if source.peek() is None:
                return None
            c4 = source.next().lower()
            if c4 not in _HEX:
                raise VDMSynatxError("A hex value is expected: "+c4+source.next(9))
            c4 = _HEX.index(c4)
            return unichr(c1*4096+c2*256+c3*16+c4)
        if c == 'c':
            return source.next()
        if c == '"':
            return '"'
        if c == "'":
            return "'"    
        if c in _OCT:
            if source.peek() is None:
                return None
            if source.peek() not in _OCT:
                raise VDMSyntaxError("An octal value expected : "+source.next(10))
            return chr(int(c)*8+int(source.next()))
        raise VDMSyntaxError("Unknown \ escape : "+c+source.next(9))
                

class VDMSyntaxError(Exception):
    pass
        
class _Stream:
    def __init__(self, string):
        self.string = string
        self.index = 0
    def peek(self):
        try:
            return self.string[self.index]
        except IndexError:
            return None
    def next(self, num=None):
        if num is None or num < 2:
            peek = self.peek()
            if peek is None:
                return None
            self.index += 1
            return peek
        else:
            index = min(len(self.string), self.index+num)
            peek = self.string[self.index:index]
            self.index = index
            return peek
    def upto(self, char):
        output = str()
        while self.peek() != char:
            if self.peek() is None:
                return output
            output += self.next()
        self.next()
        return output
    def skipSeparators(self):
        while self.peek() is not None and self.peek().isspace():
            self.next()
    def nextMatch(self, string):
        if string == self.string[self.index:self.index+len(string)]:
            self.index += len(string)
            return True
        else:
            return False

        
_HEX = "0123456789abcdef"
_OCT = "01234567"
