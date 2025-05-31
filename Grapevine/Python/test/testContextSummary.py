import unittest
import sys
sys.path.append("../src")
from contextSummary import *

class TestContextSummary(unittest.TestCase):
    def setUp(self):
        db = {"GroupsEnumerated":3,
              "Group0":0,"Group1":1,"Group2":2
              }
        self.db = db
        self.summary = ContextSummary(1, db)
        
    def test_size(self):
        #print len(self.db)
        #print self.db
        self.assertTrue(self.summary.size() == 4)
        
    def test_keySet(self):
        keySet = self.summary.keySet()
        expected = sorted(['Group1', 'Group0', 'GroupsEnumerated', 'Group2'])
        self.assertTrue(expected == sorted(keySet))
    
    def test_get(self):
        self.assertEqual(None, self.summary.get("FOO"))
        self.assertEqual(self.summary.get("Group0"), 0)
        self.assertEqual(self.summary.get("Group1"), 1)
        self.assertEqual(self.summary.get("Group2"), 2)
        self.assertEqual(self.summary.get("GroupsEnumerated"), 3)
        
    def test_put(self):
        self.assertEqual(None, self.summary.get("FOO"))
        
        self.summary.put("FOO", 100)
        self.assertEqual(100, self.summary.get("FOO"))
        
    def test_containKeys(self):
        self.assertFalse(self.summary.containsKey("FOO"))
        self.assertTrue(self.summary.containsKey("Group0"))
        
    def test_remove(self):
        self.assertTrue(self.summary.containsKey("Group0"))
        self.summary.remove("Group0")
        self.assertFalse(self.summary.containsKey("Group0"))
        
    def test_equal(self):
        db = {"GroupsEnumerated":3,
              "Group0":0,"Group1":1,"Group2":2
              }
        summary = ContextSummary(1, db)
        now = time.time()
        summary.setTimestamp(now)
        self.summary.setTimestamp(now)
        #print summary.getTimestamp()
        #print self.summary.getTimestamp()
        self.assertTrue(summary == self.summary)
        
    def test_getWireCopy(self):
        copied = self.summary.getWireCopy()
        self.assertTrue(copied == self.summary)
        
    def test_incrementHops(self):
        oldHop = self.summary.getHops()
        self.summary.incrementHops()
        newHop = self.summary.getHops()
        self.assertTrue(newHop == oldHop + 1)
        
    def test_setHops(self):
        self.summary.setHops(1001)
        self.assertTrue(1001 == self.summary.getHops())
    
    # def test_setTau(self):
    #     self.summary.setTau(1000)
    #     self.assertTrue(1000 == self.summary.getTau())
        
    def test_timestamp(self):
        db = {"GroupsEnumerated":3,
              "Group0":0,"Group1":1,"Group2":2
              }
        summary = ContextSummary(1, db)
        summary.setTimestamp(time.time())
        time.sleep(0.01)
        db2 = {"GroupsEnumerated":3,
              "Group0":0,"Group1":1,"Group2":2
              }
        summary2 = ContextSummary(1, db2)
        summary2.setTimestamp(time.time())
        
        self.assertTrue(summary.getTimestamp() < summary2.getTimestamp())
        
if __name__ == "__main__":
    unittest.main(verbosity=2)