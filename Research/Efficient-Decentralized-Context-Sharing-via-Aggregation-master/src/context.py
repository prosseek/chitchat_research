import sys
from value import *

"""
Context as of now [2013/08/14] contains only one v and hopcount
"""

class Context(object):
    def __init__(self, id, value = None, timeStamp = None, hopcount = 0):
        if type(id) is str:
            self.id = ord(id) # We need to store id as a number
        else:
            self.id = id
        self.checkTypeAndSet(value)
        self.hopcount = hopcount
        self.timeStamp = timeStamp
        
    def __eq__(self, other):
        """The equal operator
        
        We define the sameness between two contexts as follows::
        
        1. They have the same value
        2. The hopcount is the same
        3. The timestamp is the same
        
        """
        if other is None: return False
        if self.id == other.id and self.sameWithoutId(other):
           return True
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        # if self.value() is None:
        #     result = "(id(%d)None)" % (self.id)
        # else:
        #     result = "(id(%d)%d)" % (self.id, self.value())
        result = "(%d)" % (self.id) # , self.value())
        return result
        
    def __len__(self):
        return 1
        
    def getIdSet(self):
        return set([self.getId()])
        
    def getIds(self):
        return self.getIdSet()
        
    def sameWithoutId(self, other):
        if other is None: return False
        if self.v == other.v and \
           self.hopcount == other.hopcount and \
           self.timeStamp == other.timeStamp:
           return True
        return False
        
    def checkTypeAndSet(self, v):
        if type(v) is Value:
            self.v = v
        else:
            self.v = Value(v)

    def setValue(self, v):
        self.checkTypeAndSet(v)
        
    def getValue(self):
        return self.v
        
    def value(self):
        return self.v.getValue()
        
    def increaseHopcount(self):
        self.hopcount += 1
    
    def decreaseHopcount(self):
        self.hopcount -= 1;
        
    def setHopcount(self, hopcount):
        self.hopcount = hopcount
        
    def getHopcount(self):
        return self.hopcount
        
    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
    
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testContext import *

    unittest.main(verbosity=2)