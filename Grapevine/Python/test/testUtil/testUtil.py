import unittest
import sys

sys.path.append("../../src")
sys.path.append("../../src/util")

from util.util import *

class TestUtil(unittest.TestCase):  
    def setUp(self):
        pass
        
    def test_removeAll(self):
        a = [1,2,3,4,5]
        b = [3,4,5,6,7]
        c = removeAll(a, b)
        self.assertEqual(sorted([1,2]), sorted(c))
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
    