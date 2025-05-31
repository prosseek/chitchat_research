import unittest
import sys

sys.path.append("../src")

from demerge import *
from groupContext import *
from database import *
from buffer import *

a = Context('a', 10)
b = Context('b', 20)
c = Context('c', 30)
d = Context('d', 40)
e = Context('e', 50)
f = Context('f', 60)

class TestDemerge(unittest.TestCase):
    def setUp(self):
        # The input parameter should be host
        self.i = Demerge()
        
    def atest_debugging2(self):
        # 6:[(0)(1)(4)(5)(7)(9)]
        # 5:[<4(0)(4)(5)(7)><6(0)(1)(3)(5)(6)(9)><6(0)(2)(4)(5)(7)(8)><7(1)(2)(3)(5)(6)(8)(9)><7(0)(4)(5)(6)(7)(8)(9)>]
        
        # This problem reduces to 
        # **********
        # singles/usedSingles/c
        # 0:[]
        # 6:[(0)(1)(4)(5)(7)(9)]
        # 4:[<2(2)(8)><2(3)(6)><2(6)(8)><4(2)(3)(6)(8)>] ****-> <2(2)(8)><2(3)(6)>
        # **********
        
        a0 = Context(0, 10)
        a1 = Context(1, 10)
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        a5 = Context(5, 10)
        a6 = Context(6, 10)
        a7 = Context(7, 10)
        a8 = Context(8, 10)
        a9 = Context(9, 10)
        
        g0 = GroupContext(None, [a0, a4, a5, a7])
        g2 = GroupContext(None, [a0, a1, a3, a5, a6, a9])
        g5 = GroupContext(None, [a0, a2, a4, a5, a7, a8])
        g7 = GroupContext(None, [a1, a2, a3, a5, a6, a8, a9])
        g8 = GroupContext(None, [a0, a4, a5, a6, a7, a8, a9])
        
        inputDirectory = {0:[g0], 2:[g2], 5:[g5], 7:[g7], 8:[g8]}
        db = Database()
        db.singleContexts = [a0, a1, a4, a5, a7, a9]
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        
        #print result 
        e1 = GroupContext(None, [a2, a8])
        e2 = GroupContext(None, [a3, a6])
        
        e3 = GroupContext(None, [a6, a8])
        e4 = GroupContext(None, [a3, a2])
        
        expected = Database()
        expected.singleContexts = [a0, a1, a4, a5, a7, a9]
        expected.primeContexts = [e1, e2]
        expected.nonPrimeContexts = []
        
        # print result
        # print expected
        
        self.assertTrue(same(result.singleContexts,expected.singleContexts))
        if not same(result.primeContexts, expected.primeContexts):
            printList(result.primeContexts)
            printList(expected.primeContexts)
        self.assertTrue(\
            same(result.primeContexts, [e1,e2]) or same(result.primeContexts, [e3,e4])
        )
        self.assertTrue(same(result.nonPrimeContexts, expected.nonPrimeContexts))
        
    def test_debugging1(self):
        """Debugging for the bug that I found on [2013/09/20]
            024578
            {0:[<G7|id(0)11|id(4)11|id(5)11|id(6)11|id(7)11|id(8)11|id(9)11|>]| <-- 024578 => 6/9 as a new aggregation
             2:[<G6|id(1)11|id(2)11|id(3)11|id(4)11|id(6)11|id(8)11|>]|         <-- 024578 => 1/3/6 
             5:[<G6|id(0)11|id(1)11|id(4)11|id(5)11|id(7)11|id(9)11|>]|         <-- 024578 => 1/9
             7:[<G4|id(0)11|id(4)11|id(5)11|id(7)11|>]}                         <-- 024578 => No
             8:[<G6|id(0)11|id(1)11|id(2)11|id(3)11|id(4)11|id(8)11|>]|         <-- 024578 => 1/3
    
        From this configuration, 6 is found from (1/3) and (1/3/6), and then 9 is recovered from (6/9)
        And 1 is recovered from (1/9), and finally 3 **should be** recovered from (1/3). This is missing:
        
        -> 
        DB:Single:[(id(0)10)(id(1)10)(id(2)10)(id(4)10)(id(5)10)(id(6)10)(id(7)10)(id(8)10)(id(9)10)]NPrime:[<G2|id(1)10|id(3)10|>]
        """
        a0 = Context(0, 10)
        a1 = Context(1, 10)
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        a5 = Context(5, 10)
        a6 = Context(6, 10)
        a7 = Context(7, 10)
        a8 = Context(8, 10)
        a9 = Context(9, 10)
        
        g0 = GroupContext(None, [a0, a4, a5, a6, a7, a8, a9])
        g2 = GroupContext(None, [a1, a2, a3, a4, a6, a8])
        g5 = GroupContext(None, [a0, a1, a4, a5, a7, a9])
        g7 = GroupContext(None, [a0, a4, a5, a7])
        g8 = GroupContext(None, [a0, a1, a2, a3, a4, a8])
        
        inputDirectory = {0:[g0], 2:[g2], 5:[g5], 7:[g7], 8:[g8]}
        db = Database()
        db.singleContexts = [a0, a2, a4, a5, a7, a8]
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        
        #print result 
        # expected = Database()
        # expected.singleContexts = [a3, a5, a6]
        # 
        # e1 = GroupContext(None, [a1, a4])
        # e2 = GroupContext(None, [a4, a7])
        expected = Database()
        expected.singleContexts = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]
        expected.primeContexts = []
        expected.nonPrimeContexts = []
        
        self.assertTrue(same(result.singleContexts,expected.singleContexts))
        self.assertTrue(same(result.primeContexts, expected.primeContexts))
        self.assertTrue(same(result.nonPrimeContexts, expected.nonPrimeContexts))
        
        
    def test_Run1(self):
        # debugging purpose
        """
        3/5/6/(1,3,4,5)/(4,5,6,7) -> 3/5/6 and NPC (1,4) and (4,7)
        """
        a1 = Context(1, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        a5 = Context(5, 10)
        a6 = Context(6, 10)
        a7 = Context(7, 10)
        
        g3 = GroupContext(None, [a1, a3, a4, a5])
        g6 = GroupContext(None, [a4, a5, a6, a7])
        inputDirectory = {3:[g3], 6:[g6]}
        db = Database()
        db.singleContexts = [a3, a5, a6]
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        
        #print result
        expected = Database()
        expected.singleContexts = [a3, a5, a6]
        
        e1 = GroupContext(None, [a1, a4])
        e2 = GroupContext(None, [a4, a7])
        
        self.assertTrue(same(result.singleContexts,expected.singleContexts))
        # Prime (acutally shareable context) can contain e1 or e2
        # even though they share a4.
        # When e1 is selected as prime, the non-prime should contain e2 and vice versa.
        if e1 in result.primeContexts:
            self.assertTrue(same(result.primeContexts, [e1]))
            self.assertTrue(same(result.nonPrimeContexts, [e2]))
        if e2 in result.primeContexts:
            self.assertTrue(same(result.primeContexts, [e2]))
            self.assertTrue(same(result.nonPrimeContexts, [e1]))
        #print result
        
    def test_Run2(self):
        db = Database()
        
        # DB:[a,b,c][][]
        # ID:(c,d)
        # new DB -> [a,b,c,d][][]
    
        db.singleContexts = [a,b,c]
        db.primeContexts = []
        gc1 = GroupContext(None, [c,d])
        inputDirectory = {"h1":[gc1]}
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        expected = Database()
        expected.singleContexts = [a,b,c,d]
        
        self.assertTrue(same(result.singleContexts,expected.singleContexts))
        self.assertEqual(result.primeContexts, [])
        self.assertEqual(result.nonPrimeContexts, [])
        
    def test_Run3(self):
        db = Database()
        # DB:[a,b,c][(d,e)][]
        # ID: d
        # new DB -> [a,b,c,d,e][][]
        db.singleContexts = [a,b,c]
        gc1 = GroupContext(None, [d,e])
        db.primeContexts = [gc1]
        inputDirectory = {"h1":[d]}
        
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        expected = Database()
        expected.singleContexts = [a,b,c,d,e]
        
        self.assertTrue(same(result.singleContexts,expected.singleContexts))
        self.assertEqual(result.primeContexts, [])
        self.assertEqual(result.nonPrimeContexts, [])
        
    def test_Run4(self):
        db = Database()
        # DB:[a,b][<c,d>,<e,f>][]
        # Input: [e]
        # new DB -> [a,b,e,f][(c,d)][]
        db.singleContexts = [a,b]
        gc1 = GroupContext(None, [c,d])
        gc2 = GroupContext(None, [e,f])
        db.primeContexts = [gc1,gc2]
        inputDirectory = {"h1":[e]}
        
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        expected = Database()
        expected.singleContexts = [a,b,e,f]
        expected.primeContexts = [gc1]
        
        #print result
        
        #self.assertTrue(same(result.singleContexts,expected.singleContexts))
        #self.assertTrue(same(result.primeContexts,expected.primeContexts))
        #self.assertEqual(result.nonPrimeContexts, [])
        
    def test_Run5(self):
        db = Database()
        # DB:[a,b][(c,d),(e,f)][]
        # ID: e,c
        # new DB -> [a,b,c,d,e,f][][]
        db.singleContexts = [a,b]
        gc1 = GroupContext(None, [c,d])
        gc2 = GroupContext(None, [e,f])
        db.primeContexts = [gc1,gc2]
        inputDirectory = {"h1":[e], "h2":[c]}
        
        dm = Demerge(db, inputDirectory)
        result = dm.run()
        expected = Database()
        expected.singleContexts = [a,b,c,d,e,f]
        expected.primeContexts = []
        
        self.assertTrue(same(result.singleContexts,expected.singleContexts))
        self.assertTrue(same(result.primeContexts,expected.primeContexts))
        self.assertEqual(result.nonPrimeContexts, [])
        
    def testOnlyDemerge(self):
        db = Database()
        # gc1 = [a,b,c], and b
        # we expect b/[a,c]/[]
        gc1 = GroupContext(None, [a,b,c])
        inp = set([gc1, b])
        result = self.i.demerge(inp)
        expected = GroupContext(None, [a,c])
        #print result
        #print result[0][0]
        #print expected
        self.assertTrue(set(result[0]) == set([b]))
        self.assertTrue(same(set(result[1]),set([expected])))
        self.assertTrue(result[2] == [])
        
        # gc1 = [a,b,c] and a,b
        # we expect [c]/[a,b]
        gc1 = GroupContext(None, [a,b,c])
        inp = set([gc1, a, b])
        result = self.i.demerge(inp)
        
        #printList([a,b,c])
        #printList(result[0])
        #print result[1]
        
        self.assertTrue(same(result[0],[a,b,c]))
        self.assertTrue(result[1] == [])
        self.assertTrue(result[2] == [])
        
        # input = [a,b,c,d] and [a,b,c] and [a,b] and a
        # we expect [a,b,c,d]/[]/[]
        gc1 = GroupContext(None, [a,b,c,d])
        gc2 = GroupContext(None, [a,b,c])
        gc3 = GroupContext(None, [a,b])
        inp = set([gc1, gc2, gc3, a])
        result = self.i.demerge(inp)
    
        self.assertTrue(set(result[0]) == set([a,b,c,d]))
        self.assertTrue(result[1] == [])
        self.assertTrue(result[2] == [])
        
        # gc1 = [a,b,c] and d
        # we expect d/[a,b,c]/[]
        gc1 = GroupContext(None, [a,b,c])
        inp = set([gc1, d])
        result = self.i.demerge(inp)
        expected = gc1
        
        self.assertTrue(set(result[0]) == set([d]))
        self.assertTrue(same(set(result[1]),set([expected])))
        self.assertTrue(result[2] == [])
        
        # input = [a,b,c] and [b,c] and d
        # we expect [a,d]/[b,c]/[]
        gc2 = GroupContext(None, [b,c])
        inp = set([gc1, gc2, d])
        result = self.i.demerge(inp)
        expected = gc2
    
        self.assertTrue(set(result[0]) == set([a,d]))
        self.assertTrue(same(set(result[1]),set([expected])))
        self.assertTrue(result[2] == [])


if __name__ == "__main__":
    unittest.main(verbosity=2)