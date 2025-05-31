import unittest
import sys

sys.path.append("../src")

from context import *

class TestContext(unittest.TestCase):
    def setUp(self):
        self.c = Context('c')
        
    def test_getIdSet(self):
        c = Context('a',10)
        expected = set([ord('a')])
        result = c.getIdSet()
        self.assertTrue(expected == result)
        
    def test_length(self):
        c = Context('c', 10)
        result = len(c)
        self.assertTrue(result == 1)
        
    def test_equal(self):
        # == means everything is the same
        c = Context('c', 10)
        d = Context('d', 20)
        e = Context('c', 10)
        self.assertTrue(c == e)
        self.assertFalse(c == d)
        self.assertTrue(c != d)
        
    def test_sameWithoutId(self):
        # sameWithoutId means the content is the same exceptionally with id
        c = Context('c', 10)
        d = Context('d', 10)
        self.assertTrue(c.sameWithoutId(d))
        
    def test_id(self):
        a = Context('a', 10)
        self.assertEqual(a.getId(), ord('a'))
        
    def test_defaultValue(self):
        value = 100
        c = Context('c', value)
        self.assertTrue(value == c.getValue().getValue())
        
        # None test
        c = Context('c')
        self.assertTrue(c.getValue().getValue() is None)
        
    def test_getSetValue(self):
        value = 100
        self.c.setValue(value)
        self.assertTrue(value == self.c.getValue().getValue())
        
        # checkTypeAndSet
        v = Value(value)
        self.c.setValue(v)
        self.assertTrue(v == self.c.getValue())
        self.assertTrue(v.getValue() == self.c.value())
        self.assertTrue(self.c.getValue().getValue() == self.c.value())
        
    def test_setGetTau(self):
        hopcount = 12
        self.c.setHopcount(hopcount)
        self.assertEqual(hopcount, self.c.getHopcount())
        
    def test_increaseDecreaseTau(self):
        hopcount = self.c.getHopcount()
        self.c.increaseHopcount()
        self.c.decreaseHopcount()
        self.assertTrue(hopcount == self.c.getHopcount())

if __name__ == "__main__":
    unittest.main(verbosity=2)