# pyVDMC
pyVDMC is a VDMPad client library to animate VDM-SL specifications.

## VDMC object

```
  >>> from pyVDMC import VDMC
  >>> vdm = VDMC()
  >>> vdm("1+2")
  u'3'
```

  or with a specification,

```
  >>> from pyVDMC import VDMC
  >>> fib = VDMC("""
  /* fibonacci generator */
  state State of 
    n1 : nat 
    n2 : nat 
    init s == s = mk_State(0, 1)
  end 
  operations 
    next : () ==> nat 
    next() == (dcl n : nat := n1 + n2; n1 := n2; n2 := n; return n);
  """)
  >>> fib("next()")
  u'1'
  >>> fib("next()")
  u'2'
  >>> fib("next()")
  u'3'
  >>> fib("next()")
  u'5'
  >>> fib("next()")
  u'8'
  >>> fib("next()")
  u'13'
  >>> fib("next()")
  u'21'
```

## DocString and Decorators

Decorators are also available.
(Because we haven't developed value mappers, only values whose expressions can be interpreted in both VDM-SL and python is supported. Such values include numbers and lists.)

Here is another fibonacci example.
```python
from pyVDMC import *

@vdm_module('n1', 'n2')
class fibonacci:
    """
    state State of 
        n1 : nat
        n2 : nat
        init s == s = mk_State(0, 1)
    end
    operations
        next : () ==> nat
        next() == (dcl n : nat := n1 + n2; n1 := n2; n2 := n; return n)
        post RESULT = n1~ + n2~ and n1 = n2~ and n2 = RESULT;
        prev : () ==> nat
        prev() == (dcl n : nat := n2 - n1; n2 := n1; n1 := n; return n2)
        post n1 + n2 = n2~ and n2 = n1~ and n2 = RESULT;
    """
    def __init__(self):
        self.n1 = 0
        self.n2 = 1
    @vdm_method
    def next(self):
        pass
    @vdm_test
    def prev(self):
        n = self.n2 - self.n1
        self.n2 = self.n1
        self.n1 = n
        return self.n2
```
Here, a VDM-SL spec of fibonacci numbers is embedded as a docstring of the python `fibonacci` class.
The arguments of the `@vdm_module` decorator are state variables to be associated with instance variables of the python object.

The `next` method has no python implementation.
The `@vdm_method` decorator specifies that this method is animated by the VDM-SL spec.
In this particular case, `next()` in VDM-SL is evaluated and the resulting nat number is converted into python's int value.

The `prev` method has a python implemenation.
The `@vdm_test` decorator specifies that invoking this method will automatically evaluate the VDM-SL spec along with the python method, and all state variables and resulting value is compared with python's counterparts.

```
>>> from fibonacci import fibonacci
>>> f = fibonacci()
>>> f.next()
1
>>> f.next()
2
>>> f.next()
3
>>> f.next()
5
>>> f.prev()
3
>>> f.prev()
2
```

Enjoy!

---
This project is partly supported by Grant-in-Aid Scientific Research (C) 26330099
