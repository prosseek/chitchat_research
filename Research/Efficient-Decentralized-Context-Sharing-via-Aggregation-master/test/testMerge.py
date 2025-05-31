import unittest
import sys

sys.path.append("../src")

from merge import *
from database import *
from groupContext import *

a = Context('a', 10)
b = Context('b', 20)
c = Context('c', 30)
d = Context('d', 40)
e = Context('e', 50)
f = Context('f', 60)
g = Context('g', 50)
h = Context('h', 60)
i = Context('i', 60)

#db = Database()

class TestMerge(unittest.TestCase):
    def setUp(self):
        self.m = Merge()
        
    def test_runSingleCase(self):
        # merge case test when single processing is turned on
        # This is only for checking the output buffer is seetup correctly
        db = Database()
        db.singleContexts = [a,b]
        m = Merge(db)
        bf = m.run(s = True)
        #print bf
        expected = [a, b]
        self.assertTrue(same(expected, bf.singleContexts))
        
    def test_run1(self):
        db = Database()
        # a,b,g1(c,d),g2(e,f) -> g(a,b,c,d,e,f)/[a,b]
        db.singleContexts = [a,b]
        g1 = GroupContext(None, [c,d])
        g2 = GroupContext(None, [e,f])
        db.primeContexts = [g1,g2]
        
        m = Merge(db)
        bf = m.run()
        
        expected = [a,b,c,d,e,f]
        self.assertTrue(same(expected, bf.aggregatedContext.getElements()))
        #print bf.aggregatedContext
        expected = [a,b]
        self.assertTrue(same(expected, bf.singleContexts))
        
    def test_run2(self):
        # a,b,g1(c,d),g2(e,f) -> g(a,b,c,d,e,f)/[a,b]
        db = Database()
        db.singleContexts = [a,b]
        g1 = GroupContext(None, [c,d])
        g2 = GroupContext(None, [e,f])
        db.primeContexts = [g1,g2]
        
        g3 = GroupContext(None, [g,h])
        g4 = GroupContext(None, [h,i])
        db.nonPrimeContexts = [g3, g4]
        
        m = Merge(db)
        bf = m.run()
        
        expected1 = [a,b,c,d,e,f,g,h]
        #printList(bf.aggregatedContext.getElements())
        res1 = same(expected1, bf.aggregatedContext.getElements())
        expected2 = [a,b,c,d,e,f,h,i]
        #printList(bf.aggregatedContext.getElements())
        res2 = same(expected2, bf.aggregatedContext.getElements())
        
        self.assertTrue(res1 or res2)
        #print res1, res2
        #print bf.aggregatedContext
        expected = [a,b]
        self.assertTrue(same(expected, bf.singleContexts))
    
    def test_withTimeStamp(self):
        db = Database()
        # same as test_run, but the contexts has different time stamp
        b = Context('b', 20)
        b.setHopcount(10)
        db.singleContexts = [a,b]
        g1 = GroupContext(None, [c,d])
        g2 = GroupContext(None, [e,f])
        db.primeContexts = [g1,g2]
        
        m = Merge(db)
        bf = m.run()
        
        expected = [a,b,c,d,e,f]
        self.assertTrue(same(expected, bf.aggregatedContext.getElements()))
        #print bf.aggregatedContext
        expected = [a] # b should not be in the single contexts
        self.assertTrue(same(expected, bf.singleContexts))

if __name__ == "__main__":
    unittest.main(verbosity=2)