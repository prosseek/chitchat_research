import unittest
import sys

sys.path.append("../src")

from host import *
from context import *
from util import *

DEBUG = False

class TestHost(unittest.TestCase):
    def setUp(self):
        pass

    def atest_readFromSampleDataFile_sample(self):
        """TODO: enable this test
        """
        h = Host(1, None)
        h.readFromSampleDataFile("testFile/sample.txt")
        self.assertEqual(h.sample(), 11)
        self.assertEqual(h.sample(), 12)
        self.assertEqual(h.sample(), 13)
        self.assertEqual(h.sampleTime,3)
        
        self.assertEqual(h.sample(0), 11)
        
        h = Host(2, None)
        h.readFromSampleDataFile("testFile/sample.txt")
        self.assertEqual(h.sample(), 12)
        self.assertEqual(h.sample(), 13)
        self.assertEqual(h.sample(), 14)
        self.assertEqual(h.sampleTime,3)
        
        self.assertEqual(h.sample(0), 12)
        
    def test_receiveContexts(self):
        cid = 1
        c = Context(10)
        h1 = Host(cid, None)
        h1.receiveContexts(cid, [c], printFlag = DEBUG)
        result = h1.currentInputDictionary[cid]
        self.assertTrue(same(result, [c]))
        
        c2 = Context(20)
        h1.currentInputDictionary = {}
        h1.receiveContexts(cid, [c,c2], printFlag = DEBUG) # h1 receives context from node 10
        result = h1.currentInputDictionary[cid]
        self.assertTrue = same(result, [c,c2])
        
    def test_sendContextsToNeighbors(self):
        """contexts in sender of outputDictionary goes to 
           receiver's currentInputDictionary
        """
        h1 = Host(1, [2,3])
        h2 = Host(2, None)
        h3 = Host(3, None)
        neighborDictionary = {1:h1, 2:h2, 3:h3}
        
        h1.setNeighborDictionary(neighborDictionary)
        
        c = [Context(10)]
        h1.outputDictionary[2] = c #h1.setContexts(c)
        h1.outputDictionary[3] = c

        h1.sendContextsToNeighbors(printFlag=DEBUG)
        
        #print h3.receivedContexts
        result1 = h2.currentInputDictionary[1]
        result2 = h3.currentInputDictionary[1]
        # # 
        self.assertTrue(same(result1, c))
        self.assertTrue(same(result2, c))
        # self.assertEqual(resul2, c)
                
    def test_init(self):
        h = Host(1, [2,3])
        
        res = h.getNeighbors()
        expected = [2,3]
        self.assertTrue(res, expected)
        
        res = h.getId()
        expected = 1
        self.assertTrue(res, expected)
        
        h = Host(1, None)
        
        self.assertEqual([], h.getNeighbors())
        
        h.setNeighbors([2,3])
        res = h.getNeighbors()
        expected = [2,3]
        self.assertTrue(res, expected)
        
        expected = 1
        h.setId(expected)
        res = h.getId()
        self.assertTrue(res, expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)