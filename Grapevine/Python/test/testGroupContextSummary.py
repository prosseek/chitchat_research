import unittest
import sys
sys.path.append("../src")

from groupContextSummary import GroupContextSummary

class TestGroupContextSummary(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_addMemberIds(self):
        ids = [1,2,3,4,5]
        g = GroupContextSummary(101)
        g.addMemberIds(ids)
        getIds = g.getMemberIds()
        self.assertEqual(sorted(ids), sorted(getIds))
        
        # When added the same numbers, the duplicated one should not
        # be added
        g.addMemberIds(ids)
        #print g
        getIds = g.getMemberIds()
        self.assertEqual(sorted(ids), sorted(getIds))
    
    def test_getGroupCopy(self):
        ids = [1,2,3,4,5]
        g = GroupContextSummary(101)
        g.addMemberIds(ids)
        #print g
        
        copiedGroup = g.getGroupCopy()
        self.assertTrue(copiedGroup == g)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)