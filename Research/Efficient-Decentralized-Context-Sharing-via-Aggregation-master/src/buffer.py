import sys
import os.path

from util import *
from context import *

DEBUG = False

class Buffer(object):
    def __init__(self):
        self.aggregatedContext = None
        self.singleContexts = set()
        
    def __str__(self):
        res = "Buffer:"
        if self.aggregatedContext:
            res += "Aggr:%s" % self.aggregatedContext
        if self.singleContexts:
            res += "Singles:%s" % toStr(self.singleContexts)    
        return res
        
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testBuffer import *

    os.chdir("../test")
    unittest.main(verbosity=2)