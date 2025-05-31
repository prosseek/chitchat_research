import sys
from context import *
from util import *
#from contextUtil import *

"""GroupContext extends Context; it has a value and tau, but tau is not used.

GroupContext contains the member information that contributes to construct the group value.
These elements are for **simulation purpose only**. In real world, group context only keeps the value
as a Context. 

----------
Definition
----------
Element of a group context.
    When a context contributes in a Group context to constitute a value, the context is an element of a Group Context.

--------
Notation
--------
- C1(10) indicates context 1 that has a value of 10.
- We use a notation G1(C1(10),C2(20),C3(30)) to express a group context with A1, A2, and A3. 

.. Example::

  A(10), B(20), C(30)

"""

class GroupContext(Context):
    def __init__(self, value = None, elements = None):
        """g = [a,b,c]
        g1 = GroupContext(avg(g), g)
        """
        if elements is None:
            self.resetElements()
        else:
            self.setElements(elements)
            length = len(self.getIdSet())*1.0
            assert length >= 2, elements
            #print ":", length
            if value is None:
                value = sum([i.value()*len(i) for i in elements])/length
                
        Context.__init__(self, 0, value)
        
    def __str__(self):
        value = self.value()
        if value is None: value = -10000
        #string = "G(gid(%d)%d#%d:" % (self.id, value,len(self.elements))
        string = "<%d" % (len(self.elements))
        
        sortedElements = sorted(self.elements, key=lambda x:x.id)
        #print sortedElements
        
        for i in sortedElements:
            #string += "|id(%d)%d" % (i.id, i.value())
            string += "(%d)" % (i.id)
        
        string += ">"
        return string
        
    def __eq__(self, other):
        if other is None: return False
        
        members = self.getIdSet()
        assert members is not None
        
        otherMembers = other.getIdSet()
        
        return members == otherMembers
        
    def __ne__(self, other):
        #print "NEQ"
        return not self.__eq__(other)
        
    def __len__(self):
        return len(self.elements)
        
    def getIdSet(self):
        elements = self.getElements()
        idList = [i.getId() for i in elements]
        return set(idList)
        
    def getIds(self):
        return self.getIdSet()
        
    def getContext(self, id):
        """Returns the id in the element
        """
        for e in self.elements:
            if id == e.getId(): return e
        return None
        
    # elements 
    def addElements(self, value):
        self.elements = self.elements.union(value)
        self.size = len(self.elements)
        
    def getElements(self):
        return self.elements
        
    def setElements(self, memberList):
        #if type(value) is not set:
        assert type(memberList) in [set, list]
        memberList = set(memberList)
        #print memberList
        result = []
        for i in memberList:
            if type(i) is Context:
                result.append(i)
            elif type(i) is GroupContext:
                #print i
                members = i.getElements()
                for m in members:
                    result.append(m)
            else:
                raise Exception("ERROR: Only Context/GroupContext supported")
                
        self.elements = set(result)
        self.size = len(self.elements)
        #printList(result)
        
    def resetElements(self):
        self.elements = set()
        self.size = 0
        
    def getSize(self):
        return self.size
        
    # value
    def calculateAverage(self):
        sum = 0
        for v in self.elements:
            sum += v.getValue().getValue()
        return sum/self.getSize()
    
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testGroupContext import *

    unittest.main(verbosity=2)