import unittest
import sys
import os.path

# src should come first as the util.groupUtils things
sys.path.append(os.path.abspath("../../src"))

#print sys.path

from util.groupUtils import *
from contextSummary import *
from groupContextSummary import *

class TestGroupUtils(unittest.TestCase):  
    def setUp(self):
        db = {"GroupsEnumerated":3,
              "Group0":101,"Group1":102,"Group2":103,
              "IdsAggregated":5,
              "Id0":10, "Id1":20, "Id2":30, "Id3":40, "Id4":50
              }
        self.summary = ContextSummary(1, db)
        self.aggregatedIds = [10,20,30,40,50]
        
        db2 = {"GroupsEnumerated":3,
              "Group0":101,"Group1":103,"Group2":104,
              "IdsAggregated":3,
              "Id0":10, "Id1":20, "Id2":30
              }
        self.summary2 = ContextSummary(2, db2)
        self.aggregatedIds2 = [10,20,30]
        
        # No common aggregation with db
        db3 = {"GroupsEnumerated":3,
              "Group0":101,"Group1":104,"Group2":105,
              "IdsAggregated":3,
              "Id0":110, "Id1":120, "Id2":130
              }
        self.summary3 = ContextSummary(3, db3)
        self.aggregatedIds3 = [110,120,130]
        
        groupDbNull = {}
        self.groupSummaryNull = GroupContextSummary(100, groupDbNull)
        
        # groupSummary that I use for test
        groupDb = {"MembersEnumerated":3,
                   "Member0":1, "Member1":2, "Member2":3}
        self.groupSummaryMembers = [1,2,3]
        self.groupSummary = GroupContextSummary(101, groupDb)
              
    def test_getDeclaredMemberships(self):
        groups = getDeclaredMemberships(self.summary)
        # http://stackoverflow.com/questions/7828867/how-to-efficiently-compare-two-unordered-lists-not-sets-in-python
        self.assertTrue(sorted(groups) == sorted([101,102,103]))
        
    def test_addDeclaredGroupMembership(self):
        self.assertFalse(declaresGroupMembership(self.summary, 100))
        groups = getDeclaredMemberships(self.summary)
        self.assertTrue(len(groups) == 3)
        
        addDeclaredGroupMembership(self.summary, 100)
        
        self.assertTrue(declaresGroupMembership(self.summary, 100))
        groups = getDeclaredMemberships(self.summary)
        self.assertTrue(len(groups) == 4)
        
    def test_declaresGroupMembership(self):
        self.assertFalse(declaresGroupMembership(self.summary, 4))
        self.assertTrue(declaresGroupMembership(self.summary, 101))
        #print self.summary
        
    def test_addGroupMember(self):
        addGroupMember(self.groupSummaryNull, 1200)
        self.assertEqual(getGroupMembers(self.groupSummaryNull), [1200])
        
    def test_getGroupMembers(self):
        members = getGroupMembers(self.groupSummaryNull)

    def test_getGroupMembers(self):
        groupDb = {}
        groupSummary = ContextSummary(100, groupDb)
        result = getGroupMembers(groupSummary)
        self.assertTrue(result == [])
        
        result = getGroupMembers(self.groupSummary)
        #print result
        self.assertTrue(sorted(result) == sorted(self.groupSummaryMembers))
        
    def test_setGroupMembers(self):
        newMembers = []
        setGroupMembers(self.groupSummary, newMembers)
        result = getGroupMembers(self.groupSummary)
        self.assertFalse(result)
        
    #def test_setGroupMembers_biggerThanBefore(self):
        newMembers = [1,2,3,4,5,6,7]
        setGroupMembers(self.groupSummary, newMembers)
        result = getGroupMembers(self.groupSummary)
        self.assertTrue(sorted(newMembers) == sorted(result))
        
        # retrieve the size of the members and compare
        size = self.groupSummary.get(MEMBERS_ENUMERATED)
        self.assertEqual(len(newMembers), size)
        
    #def test_setGroupMembers_smallerThanBefore(self):
        newMembers = [1]
        setGroupMembers(self.groupSummary, newMembers)
        result = getGroupMembers(self.groupSummary)
        self.assertTrue(sorted(newMembers) == sorted(result))
        
        size = self.groupSummary.get(MEMBERS_ENUMERATED)
        self.assertEqual(len(newMembers), size)
        
    def test_isAggregated(self):
        #isAggregated(summary, idToCheck)
        self.assertTrue(isAggregated(self.summary, 10))
        self.assertFalse(isAggregated(self.summary, 1000))
    
    def test_haveNoCommonAggregation(self):
        # summary2 has common aggregation, so false returned
        self.assertFalse(haveNoCommonAggregation(self.summary, self.summary2))
        # summary3 has no common aggregation, so true returned
        self.assertTrue(haveNoCommonAggregation(self.summary, self.summary3))
        
    def test_getAggregatedIds(self):
        result = getAggregatedIds(self.summary)
        #print self.aggregatedIds
        self.assertTrue(sorted(self.aggregatedIds) == sorted(result))
        
    def test_addAggregatedId(self):
        ids = self.summary.get(IDS_AGGREGATED)
        addAggregatedId(self.summary, 200)
        
        # the ids has the total number:
        # [1,2,3,4,5] --> 5, but the index is 0,1,2,3,4,*5
        # So ids should be the newly assigned index
        value = self.summary.get(ID_AGGREGATION_PREFIX + str(ids))
        
        self.assertEqual(self.summary.get(IDS_AGGREGATED),ids + 1)
        self.assertEqual(value, 200)
        
    def test_setAggregatedIds(self):
        ids = [41,42,43,44,45,46,47]
        setAggregatedIds(self.summary, ids)
        
        numberOfIds = self.summary.get(IDS_AGGREGATED)
        self.assertEqual(numberOfIds, len(ids))
        
    def test_aggregateIntoGroupSummary(self):
        #print self.groupSummary
        aggregatedSize1 = self.summary.get(IDS_AGGREGATED)
        aggregatedSize2 = self.groupSummary.get(IDS_AGGREGATED)
        
        self.assertEqual(len(self.aggregatedIds), aggregatedSize1)
        self.assertEqual(None, aggregatedSize2)
        
        aggregateIntoGroupSummary(self.groupSummary, self.summary)
        aggregatedSize2 = self.groupSummary.get(IDS_AGGREGATED)
        self.assertEqual(len(self.aggregatedIds), aggregatedSize2)
        #print self.groupSummary
        
    def test_updateGroupAggForOneSummary(self):
        summary = self.summary
        # print self.summary
        # 'IdsAggregated': 5, <-- 5 aggregations 
        #  'Id0': 10, 'Id4': 50, 'Id2': 30, 'Id3': 40, , 'Id1': 20
        # 'GroupsEnumerated': 3 <-- 3 groups summary is in
        # 'Group1': 102, 'Group0': 101, 'Group2': 103
        
        groupSummary = self.groupSummary
        #print groupSummary
        # {'MembersEnumerated': 3, 'Member0': 1, 'Member1': 2, 'Member2':3}
        
        # if (declaresGroupMembership(summary, gid) or summary.getId() == gid) \
        #    and not isAggregated(groupSummary, summary.getId) \
        #    and haveNoCommonAggregation(groupSummary, summary):
        
        # 1. summary should be a member 
        self.assertTrue(declaresGroupMembership(summary, groupSummary.getId()))
        # 2. not isAggregated(groupSummary, summary.getId)
        self.assertFalse(isAggregated(groupSummary, summary.getId()))
        # 3. haveNoCommonAggregation(groupSummary, summary)
        self.assertTrue(haveNoCommonAggregation(groupSummary, summary))
        
        # Then aggregateIntoGroupSummary(groupSummary, summary)
        #_updateGroupAgg(groupSummary, summary)
        # Just copied the code from test_aggregateIntoGroupSummary
        aggregatedSize1 = self.summary.get(IDS_AGGREGATED)
        aggregatedSize2 = self.groupSummary.get(IDS_AGGREGATED)
        
        self.assertEqual(len(self.aggregatedIds), aggregatedSize1)
        self.assertEqual(None, aggregatedSize2)
        updateGroupAggForOneSummary(groupSummary, summary)
        aggregatedSize2 = self.groupSummary.get(IDS_AGGREGATED)
        self.assertEqual(len(self.aggregatedIds), aggregatedSize2)
        
        # TODO
        # Check the summary.getId() == gid case
        summary = self.groupSummary
        self.assertTrue(summary.getId() == groupSummary.getId())
        
    def test_updateGroupAgg(self):
        summaries = [self.summary, self.summary2, self.summary3]
        updateGroupAgg(self.groupSummary, summaries)
        
if __name__ == "__main__":

    unittest.main(verbosity=2)
    