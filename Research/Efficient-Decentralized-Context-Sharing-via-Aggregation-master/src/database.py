import sys
import os.path

from util import *
from context import *

DEBUG = False

class Database(object):
    """
    TODO:

    primeContexts and nonPrimeContexts category is wrong
    It should be shareableContexts and nonSharableContexts so that
    shareable + nonSharable = group
    """
    def __init__(self, singleContexts = None, primeContexts = None, nonPrimeContexts = None):
        if singleContexts is None:
            singleContexts = set()
        if primeContexts is None:
            primeContexts = set()
        if nonPrimeContexts is None:
            nonPrimeContexts = set()
        
        self.singleContexts = singleContexts
        self.primeContexts = primeContexts
        self.nonPrimeContexts = nonPrimeContexts
        # sent history
        self.sentHistory = {}
        
    def __str__(self):
        res = "DB:"
        if self.singleContexts:
            res += "Single:%s" % toStr(sorted(self.singleContexts, key=lambda i: i.id))
        if self.primeContexts:
            res += "Prime:%s" % toStr(sorted(self.primeContexts, key=len))
        if self.nonPrimeContexts:
            res += "NPrime:%s" % toStr(self.nonPrimeContexts)
        res += "\n"    
        return res
        
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    import testDatabase

    os.chdir("../test")
    unittest.main(verbosity=2)