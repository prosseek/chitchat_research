import unittest
import sys

sys.path.append("../src")

from groupContext import *
from context import *

a = Context('a',10)
b = Context('b',20)
c = Context('c',30)
d = Context('d',40)
g = GroupContext(None, [a,b,c,d])

class TestGroupContext(unittest.TestCase):
    def setUp(self):
        #pass
        self.g = GroupContext()
        
    def test_stringGroupContext(self):
        #g = GroupContext(None, [d,c,b,a])
        result = g.__str__()
        #print result
        expected = "<4(97)(98)(99)(100)>"
        self.assertTrue(result == expected)
        
    def test_groupInGroup(self):
        #print "T"
        g1 = GroupContext(None,[c,d])
        g = GroupContext(None,[a,b,g1])
        
        #print g.getIdSet()
        expected = (10+20+30+40)/(4.0)
        result = g.value()
        #print expected,result
        #print g
        self.assertTrue(expected == result)
    
    def test_setupWithoutValueButWithElements(self):
        g = GroupContext(None, [a,b,c,d])
        result = g.value()
        expected = (10+20+30+40)/(4*1.0)
        self.assertTrue(expected == result)
        
    def test_getContext(self):
        result = g.getContext(ord('a'))
        expected = a
        self.assertTrue(expected == result)
        
    def test_getIdSet(self):
        g1 = GroupContext(15, [a,b])
        result = g1.getIdSet()
        expected = set([ord('a'), ord('b')])
        self.assertTrue(result == expected)
        
        g2 = GroupContext(15, [c,d])
        result = g2.getIdSet()
        expected = set([ord('c'), ord('d')])
        self.assertTrue(result == expected)
        
    def test_equal(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [a,b])
        g3 = GroupContext(None, [b,c])
        g4 = GroupContext(None, [c,d])
        
        # print g1
        # print g2
        #self.assertEqual(g1, g2)#(g1 != g2)
        self.assertTrue(g1 == g2)
        self.assertTrue(g2 != g3)
        self.assertTrue(g3 != g4)
        
    def test_length(self):
        inp = [a,b,c]
        avg = sum([i.value() for i in inp])/len(inp)
        g = GroupContext(avg, inp)
        self.assertEqual(len(inp),len(g))
        
    def test_groupContextWithDefaultValues(self):
        inp = [a,b,c]
        avg = sum([i.value() for i in inp])/len(inp)
        g = GroupContext(avg, inp)
        self.assertEqual(g.calculateAverage(), avg)
        self.assertEqual(g.getElements(), set([a,b,c]))
        
    def test_addElements(self):
        self.g.addElements([a,b,c])
        self.g.addElements([b,c,d])

        # Ceheck if there is no duplicate
        self.assertEqual(set([a,b,c,d]), self.g.getElements())
        self.assertEqual(4, self.g.getSize())
    
    def test_resetElement(self):
        self.g.setElements(set([a,b,c,d])) # used set type conversion
        self.assertEqual(set([a,b,c,d]), self.g.getElements())
        self.assertEqual(4, self.g.getSize())
        
        self.g.setElements([a,d]) # input as a list, it should be change typed into set
        self.assertEqual(set([a,d]), self.g.getElements())
        self.assertEqual(2, self.g.getSize())
        
    def test_setElement(self):
        x = Context('x', 100)
        y = Context('y', 200)
        z = Context('z', 300)
        gx = GroupContext(None, [x,y,z])
        
        g = GroupContext()
        #print "\n\n\n\nNOW"
        g.setElements([a,b,c,d,gx]) # used set type conversion
        #printList(g.getElements())
        self.assertEqual(set([a,b,c,d,x,y,z]), g.getElements())
        #self.assertEqual(4, self.g.getSize())
        
    def test_getValue(self):
        self.g.setElements(set([a,b,c,d]))
        self.assertEqual((10+20+30+40)/4, self.g.calculateAverage())
        

if __name__ == "__main__":
    unittest.main(verbosity=2)