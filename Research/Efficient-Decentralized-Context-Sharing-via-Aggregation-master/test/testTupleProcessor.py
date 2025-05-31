import unittest
import sys

sys.path.append("../src")

from tupleProcessor import *

class TestTupleProcessor(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_add(self):
        t = TupleProcessor((1,2,3,4))
        expected = map(lambda x: 3*x, t.getTuple())
        t += (1,2,3,4)
        t += (1,2,3,4)

        r = t.getTuple()
        self.assertEqual(r, tuple(expected))

    def test_divide(self):
        t = TupleProcessor((1,2,3,4))
        expected = map(lambda x: x/3.0, t.getTuple())
        t /= 3
        r = t.getTuple()
        self.assertEqual(r, tuple(expected))

    def test_emptyInitialization(self):
        t = TupleProcessor()
        t += (1,2,3,4)
        t += (1,2,3,4)
        expected = (2,4,6,8)
        self.assertEqual(expected, t.getTuple())

if __name__ == "__main__":
    unittest.main(verbosity=2)