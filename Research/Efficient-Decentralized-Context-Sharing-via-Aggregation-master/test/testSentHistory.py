import unittest
import sys

sys.path.append("../src")

from context import *
from groupContext import *
from sentHistory import *

a = Context('a', 10)
b = Context('b', 20)
c = Context('a', 10)
d = Context('d', 10)
g = GroupContext(None, [a,b])
        
class TestSentHistory(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_noHistory(self):
        h = SentHistory()
        result = h['h1']
        self.assertTrue(result == [])
        
    def test_index(self):
        h = SentHistory()
        h.add('h1', a)
        result = h['h1']
        self.assertTrue(list(result)[0] == a)
        
    def test_addList(self):
        h = SentHistory()
        h.add('h1', [a, b, c, d])
        result = h.get('h1')
        self.assertTrue(same(result, [a,b,c,d]))
        
    def test_add(self):
        h = SentHistory()
        h.add('h1', a)
        result = h.get('h1')
        self.assertTrue(list(result)[0] == a)
        
    def test_addDictionary(self):
        h = SentHistory()
        d1 = {'h1':[a,b,c]}
        h.addDictionary(d1)
        result = h.get('h1')
        self.assertTrue(same(list(result), [a,b,c]))
        
        d2 = {'h1':[g]}
        h.addDictionary(d2)
        result = h.get('h1')
        self.assertTrue(same(list(result), [a,b,c,g]))
        #print h.get('h1')
        
    def test_get(self):
        h = SentHistory()
        h.add('h1',g)
        h.add('h1',c)
        l = sorted(list(h.get('h1')), key=len)
        #printList(l)
        self.assertTrue(l[0] == c)
        self.assertTrue(l[1] == g)
        
        
    def test_sent(self):
        a = Context('a', 10)
        b = Context('b', 20)
        c = Context('a', 10)
        
        h = SentHistory()
        h.add('h1', a)
        self.assertTrue(h.sent('h1',a))
        self.assertFalse(h.sent('h2',a))
        
        # different context, but same content
        self.assertTrue(h.sent('h1',c))
        
        #print h.sent('h1',c)

if __name__ == "__main__":
    unittest.main(verbosity=2)