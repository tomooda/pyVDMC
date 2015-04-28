# pyVDMC
pyVDMC is a VDMPad client library to animate VDM-SL specifications.

usage:

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
Enjoy!
