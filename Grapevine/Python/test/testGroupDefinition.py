import unittest
import sys
sys.path.append("../src")

from groupDefinition import *
from contextSummary import *
from groupContextSummary import *
from util.groupUtils import *

class TestGroupDefinition(unittest.TestCase):
    def setUp(self):
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":101,"Group2":102
             }
        self.summary = ContextSummary(1, db)
        
        self.groupDb = {"MembersEnumerated":3,
                   "Member0":5, "Member1":2, "Member2":3} # 1 is not in the member

        self.groupDb2 = {"MembersEnumerated":3,
                   "Member0":5, "Member1":2, "Member2":15} # only 13 is new member
                   
    def test_handleContextSummary1(self):
        groupSummary = GroupContextSummary(100, self.groupDb)
        
        g = GroupDefinition(500)
        
        # after the operation, 1 is now in the member
        self.assertFalse(1 in getGroupMembers(groupSummary))
        g.handleContextSummary(groupSummary, self.summary)
        self.assertTrue(1 in getGroupMembers(groupSummary))
        
    def test_handleContextSummary2(self):
        # gid 110 is not in db
        groupSummary = GroupContextSummary(110, self.groupDb)
        
        g = GroupDefinition(500)
        
        # after the operation, 1 is still "not" in the member, as gid 
        # is not one of its groupEnumerated
        self.assertFalse(1 in getGroupMembers(groupSummary))
        g.handleContextSummary(groupSummary, self.summary)
        self.assertFalse(1 in getGroupMembers(groupSummary))
        
    def test_handleGroupSummary(self):
        currentGroupSummary = GroupContextSummary(110, self.groupDb)
        newGroupSummary = GroupContextSummary(101, self.groupDb2)
        
        g = GroupDefinition(500)
        
        self.assertEqual(sorted([5,2,3]), sorted(getGroupMembers(currentGroupSummary)))
        g.handleGroupSummary(currentGroupSummary, newGroupSummary)
        self.assertEqual(sorted([5,2,3,15]), sorted(getGroupMembers(currentGroupSummary)))
        
        # 15 should be added
        
if __name__ == "__main__":
    unittest.main(verbosity=2)