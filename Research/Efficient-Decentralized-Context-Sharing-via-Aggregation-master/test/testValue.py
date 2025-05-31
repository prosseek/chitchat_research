import unittest
import sys

sys.path.append("../src")

from value import *

class TestValue(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_getSet(self):
        a = Value(10)
        self.assertTrue(10 ==a.getValue())
        
        a.setValue(20)
        self.assertTrue(20 ==a.getValue())
        
    def test_range(self):
        a = Value(20)
        self.assertTrue(a.getRange() == [20,20])
        a.setRange([20,30])
        self.assertTrue(a.getRange() == [20,30])
        
    def test_equality(self):
        a = Value(20, [20,20])
        b = Value(30, [20,40])
        self.assertTrue (a != b)
        c = Value(20, [20,20])
        
        # a and c are different in reference
        self.assertFalse(id(a) == id(c))
        # but they are the same in value
        self.assertTrue(a == c)

if __name__ == "__main__":
    unittest.main(verbosity=2)