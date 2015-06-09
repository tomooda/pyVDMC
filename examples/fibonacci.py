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
        """
        generates the next fibonacci number
        """
        pass
    #@vdm_test
    @vdm_method
    def prev(self):
        """
        rollbacks to the previous fibonacci number
        """
        n = self.n2 - self.n1
        self.n2 = self.n1
        self.n1 = n
        return self.n2
