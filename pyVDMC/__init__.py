"""
pyVDMC
~~~~~~

pyVDMC is a VDMPad client library to animate VDM-SL specifications.
usage:

  >>> from pyVDMC import VDMC
  >>> vdm = VDMC()
  >>> vdm("1+2")
  u'3'

  or with a specification,
  >>> from pyVDMC import VDMC
  >>> fib = VDMC('state State of n1 : nat n2 : nat init s == s = mk_State(0, 1) end operations next : () ==> nat next() == (dcl n : nat := n1 + n2; n1 := n2; n2 := n; return n);')
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

Enjoy!
"""

from __future__ import absolute_import
from .VDMC import DEFAULT_SERVER, VDMError, TestFailed, VDMC, vdm_module, vdm_method, vdm_test
from .VDMValue import Composite, Quote, Token, VDM_TRUE, VDM_FALSE, VDM_NUM, VDM_CHAR, VDM_QUOTE, VDM_TOKEN, VDM_SET, VDM_SEQ, VDM_MAP, VDM_TUPLE, VDM_COMPOSITE, VDM_NIL, VDM_STRING
from .Reader import VDMReader, VDMSyntaxError
from .Writer import VDMWriter
