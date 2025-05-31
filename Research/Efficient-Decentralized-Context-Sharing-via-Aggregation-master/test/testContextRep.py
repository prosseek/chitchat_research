import unittest
import sys
from util import *

sys.path.append("../src")

from ContextRep import *

class TestContextRep(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_A(self):
        expected = [0,1,2,3,4,5,10,12,100, 444,123,500, 499, 443,321, 222]
        c = ContextRep(10.32, expected)
        r1 = c.aggregationToBytestream()
        #print len(r1) == 71 (500/8 + 1 + 8)
        self.assertTrue(500/8 + 1 + 8 == len(r1))
        r2 = c.byteStreamToAggregation()
        self.assertTrue(same(expected, r2))

if __name__ == "__main__":
    unittest.main(verbosity=2)

