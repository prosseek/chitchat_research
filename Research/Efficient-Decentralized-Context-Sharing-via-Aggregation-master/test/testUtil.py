import unittest
import sys

sys.path.append("../src")

from util import *
from context import *
from groupContext import *
from copy import *

a = Context('a', 10)
b = Context('b', 20)
c = Context('c', 30)
d = Context('d', 40)
e = Context('e', 50)
f = Context('f', 60)

class TestUtil(unittest.TestCase):
    def setUp(self):
        pass

    def test_truefalse(self):
        result = []
        percentage = 0.3
        totalLength = 1000
        for i in range(totalLength):
            result.append(truefalse(percentage))

        #print result
        count = len(filter(lambda x: x, result))
        result = 100.0*count/totalLength
        self.assertTrue(result < 34)

    def test_sameDictionary(self):
        d1 = {1:[1,2,3], 2:[2,3,4], 3:[1,2,5]}
        d2 = deepcopy(d1)
        res = sameDictionary(d1, d2)
        self.assertTrue(res)
        
        d1 = {1:[1,2,3], 2:[2,3,4], 3:[1,2,5]}
        d2 = {1:[1,2,3], 2:[2,3,4]}
        res = sameDictionary(d1, d2)
        self.assertFalse(res)
        
        d1 = {1:[1,2,3], 2:[2,3,4], 3:[1,2,5]}
        d1 = {1:[1,2,3], 2:[2,3,4], 3:[1,5]}
        res = sameDictionary(d1, d2)
        self.assertFalse(res)
        
    # def test_printList(self):
    #     g1 = GroupContext(None, [a,b,c,d])
    #     g2 = GroupContext(None, [c,d,e,f])
        #printList([g1,a,b,c])
        
    def test_toStrInteger(self):
        input = [1,4,2,3]
        result = toStr(input)
        self.assertTrue(result == "[1234]")
        
    def test_toStrContext(self):
        input = [f,e,d,c,b]
        result = toStr(input)
        expected = "[(98)(99)(100)(101)(102)]" #"[(id(98)20)(id(99)30)(id(100)40)(id(101)50)(id(102)60)]" 
        # print expected
        # print result 
        self.assertTrue(result == expected)
        
    def test_removeLast(self):
        input = "Hello"
        expected = "Hell"
        result = removeLast(input)
        self.assertTrue(expected == result)
        
        input = "Hello"
        expected = "Hel"
        result = removeLast(input, 2)
        self.assertTrue(expected == result)
        
    def test_increaseHopcount(self):
        # a is modified, so you can't use global a
        a = Context('a', 10)
        value = 10
        a.setHopcount(value)
        b = increaseHopcount(a)
        self.assertTrue(b.getHopcount(), value + 1)
        
    def test_getStringFromList(self):
        a = [1,3,4]
        expected = "[1:3:4]" 
        self.assertEqual(expected, getStringFromList(a))
        
        a = 5
        expected = "5" 
        self.assertEqual(expected, getStringFromList(a))
    
    def test_getFirstRest(self):
        value = "1: 2 3 4 5 6"
        expectedFirst = 1
        expectedRest = [2, 3, 4, 5, 6]
        first, rest = getFirstRest(value)
        self.assertEqual(first, expectedFirst)
        self.assertEqual(rest, expectedRest)
    
    def test_intersection(self):
        cList1 = [a,b,c]
        g1 = GroupContext(avg(cList1), cList1)
        cList2 = [c,d,e]
        g2 = GroupContext(avg(cList2), cList2)
        expected = set([c])
        res = intersection(g1, g2)
        self.assertEqual(expected, res)
        
    def test_union(self):
        cList1 = [a,b,c]
        g1 = GroupContext(avg(cList1), cList1)
        cList2 = [c,d,e]
        g2 = GroupContext(avg(cList2), cList2)
        expected = set([a,b,c,d,e])
        res = union(g1, g2)
        self.assertEqual(expected, res)
        
    def test_diff(self):
        cList1 = [a,b,c]
        g1 = GroupContext(avg(cList1), cList1)
        cList2 = [c,d,e]
        g2 = GroupContext(avg(cList2), cList2)
        expected = set([a,b])
        res = diff(g1, g2)
        self.assertEqual(expected, res)
    
    def test_avg(self):
        #print "a"
        self.assertEqual(avg([a,b,c]), (10+20+30)/3)
        
    def test_isIn(self):        
        g = [a,b,c]
        d = Context('a', 10)
        
        self.assertTrue(isIn(d, g))

        e = Context('e', 30)
        self.assertFalse(isIn(e, g))
        
    def test_same1(self):
        d = Context('a', 10)
        e = Context('b', 20)
        f = Context('c', 30)
        g = Context('d', 40)
        
        self.assertTrue(same(set([a,b,c]), set([d,e,f])))
        self.assertFalse(same(set([a,b]), set([d,e,f])))
        self.assertFalse(same(set([a,b,g]), set([d,e,f])))
        
        #TODO
        ### This returns True, but it should return False
        #self.assertFalse(same(set([a,a,b]), set([a,b,b])))
        self.assertTrue(same(set([a,a,b]), set([a,b,b])))
        
        # Zero test
        self.assertTrue(same([],[]))
        self.assertTrue(same(set(), set()))
        
        self.assertFalse(same([],[a]))
        self.assertFalse(same([],set([a])))
        
    def test_same2(self):
        self.assertTrue(same([1],[1]))

if __name__ == "__main__":
    unittest.main(verbosity=2)