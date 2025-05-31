import unittest
import sys
sys.path.append("../src")

from contextHandler import *
from groupContextSummary import *

class TestContextHandler(unittest.TestCase):
    def setUp(self):
        ContextHandler.singleton = None # Refresh
        self.c = ContextHandler().getInstance()
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":102,"Group2":103,
              "IdsAggregated":5,
              "Id0":10, "Id1":20, "Id2":30, "Id3":40, "Id4":50
              }
        self.summary = ContextSummary(1, db)
        
        db2 = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        self.summary2 = ContextSummary(22, db2)
        #print GroupContextSummary(1000)
        #dprint(self.c.getGroupContexts())
        
    def tearDown(self):
        pass
        #ContextHandler.singleton = None
        #GroupContextSummary(100)
        
    def test_setMyContext(self):
        self.c.setMyContext(self.summary)
        self.assertEqual(self.summary, self.c.getMyContext())
        
    def test_setReceivedSummaries(self):
        self.c.setReceivedSummaries({1:self.summary})
        self.assertEqual(self.summary, self.c.getReceivedSummaries()[1])
        
    def test_getInstance(self):
        ch = ContextHandler.getInstance()
        ch2 = ContextHandler.getInstance()
        self.assertEqual(ch, ch2) # checking the references
        
    # def test_getGroupContext(self):
    #     getGroupContext
        
    def test_setupGroupDefinition(self):
        g = GroupDefinition(100)
        self.c.setupGroupDefinition(g)
        
        # it just creates empty GroupSummary, but it's not None
        self.assertTrue(self.c.getGroupContext(100) is not None)
        self.assertTrue(self.c.getGroupDefinition(100) is not None)
        
    def test_performGroupFormations(self):
        # set group definistions in ContextHandler
        g = GroupDefinition(100); groupDefinitions = {100:g}
        self.c.setupGroupDefinition(g)
        
        # You *should* get group summary from the getGroupContext method
        groupSummary = self.c.getGroupContext(100)
        
        # myContext is from the summary with id 1
        myContext = self.summary 
        
        # handle it to make groupSummary to contain [1]
        g.handleContextSummary(groupSummary, myContext)
        
        # before -> there should be only [1]
        members = getGroupMembers(groupSummary)
        self.assertTrue(sorted([1]) == sorted(members))
        
        # after -> we have summaries with id 22
        summaries = [self.summary2]
        self.c.performGroupFormations(groupDefinitions, summaries)
        groupSummary = self.c.getGroupContext(100)
        members = getGroupMembers(groupSummary)

        self.assertTrue(sorted([1,22]) == sorted(members))

    def test_addGroupDefinition(self):
        # addGroupDefiniton
        # assumes myContext and received summaries are already set
        #dprint(self.c.getGroupContext(100))
        g = GroupDefinition(100)
        #dprint(self.c.getGroupContext(100))
        self.c.setMyContext(self.summary)
        #dprint(self.c.getGroupContext(100))
        self.c.setReceivedSummaries({22:self.summary2})
        #dprint(self.c.getGroupContext(100))
        self.assertTrue(self.c.getGroupContext(100) is None)
        
        self.c.addGroupDefinition(g)

        groupSummary = self.c.getGroupContext(100)
        members = getGroupMembers(groupSummary)
        self.assertTrue(sorted([1, 22]) == sorted(members))
        
    def test_updateLocalSummary(self):
        # setup for group definitions
        g = GroupDefinition(100); groupDefinitions = {100:g}
        self.c.setupGroupDefinition(g)
        
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        summary = ContextSummary(7, db)
        
        #print self.c.groupContexts[100] -> (100):{}
        groupSummary = self.c.groupContexts[100]
        self.assertTrue([] == getGroupMembers(groupSummary))
        self.c.updateLocalSummary(summary)
        groupSummary = self.c.groupContexts[100]
        self.assertTrue([7] == getGroupMembers(groupSummary))
        #print self.c.groupContexts[100] --> (100):{'MembersEnumerated': 1, 'Member0': 7}
        
    def test_removeLocalSummary(self):
        self.c.setMyContext(self.summary)
        context = self.c.getMyContext()
        self.assertTrue(context is not None)
        
        self.c.removeLocalSummary()
        context = self.c.getMyContext()
        self.assertTrue(context is None)
        
    def test_handleIncomingSummaries_longerHops(self):
        # Old summary has tau 10 
        self.c.setMyContext(self.summary)
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        summary = ContextSummary(7, db)
        summary.setHops(10)
        
        # input of setReceivedSummaries should be dictionary
        self.c.setReceivedSummaries({7:summary})
        #print self.c.receivedSummaries
        
        db2 = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        newsummary = ContextSummary(7, db2)
        newsummary.setHops(3)

        updatedSummaries = self.c.getReceivedSummaries()
        
        #print updatedSummaries[7].getTau()
        # summary id 7 and tau 3
        receivedSummaries = [newsummary] # new tau is 3
        self.c.handleIncomingSummaries(receivedSummaries)
        
        # check 
        updatedSummaries = self.c.getReceivedSummaries()
        #print updatedSummaries[7].getTau()
        # 10 is replaced by 4 (3 + 1)
        self.assertTrue(updatedSummaries[7].getHops() == 4)
        
    def test_handleIncomingSummaries_newerTimestamp(self):
        # Old summary has tau 10 
        self.c.setMyContext(self.summary)
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        summary = ContextSummary(7, db)
        summary.setHops(10)
        summary.setTimestamp(summary.getTimestamp() - 100)
        
        # input of setReceivedSummaries should be dictionary
        self.c.setReceivedSummaries({7:summary})
        db2 = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        newsummary = ContextSummary(7, db2)
        newsummary.setHops(16)

        updatedSummaries = self.c.getReceivedSummaries()
        
        #print updatedSummaries[7].getTau()
        # summary id 7 and tau 3
        receivedSummaries = [newsummary] # new tau is 3
        self.c.handleIncomingSummaries(receivedSummaries)
        
        # check 
        updatedSummaries = self.c.getReceivedSummaries()
        # print updatedSummaries[7].getTau()
        # 10 is replaced by 17 (16 + 1)
        self.assertTrue(updatedSummaries[7].getHops() == (16 + 1))
        
    def test_get_from_myContext(self):
        summary = self.summary
        uid = summary.getId()
        self.c.setMyContext(summary)
        #print self.c.get(7)
        #print summary
        self.assertTrue(summary == self.c.get(uid))
        self.assertFalse(id(summary) == id(self.c.get(uid)))
        
    def test_get_from_group(self):
        # get returns from groupContext
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        #self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        self.assertTrue(self.c.groupContexts[100] == self.c.get(100))
        self.assertFalse(id(self.c.groupContexts[100]) == id(self.c.get(100)))
        
    def test_get_from_receivedSummaries(self):
        # get returns from groupContext
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        self.assertTrue(self.c.receivedSummaries[22] == self.c.get(22))
        self.assertFalse(id(self.c.receivedSummaries[22]) == id(self.c.get(22)))
        
    def test_setTau(self):
        newTau = 100
        self.c.setTau(newTau)
        self.assertTrue(self.c.getTau() == newTau)
        
    def test_getReceivedSummaries(self):
        # when there is only myContext
        self.c.setMyContext(self.summary)
        self.assertTrue(len(self.c.getSummariesToSend()) == 1)
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        #print self.c.getReceivedSummaries()
        
        expected = sorted([1, 100])
        result = []
        
        for i in self.c.getSummariesToSend():
            result.append(i.getId())
        self.assertTrue(expected == sorted(result))
        #print self.c.getSummariesToSend()
        
    def test_getReceivedSummaries_biggerHops(self):
        # when there is only myContext
        self.c.setMyContext(self.summary)
        self.assertTrue(len(self.c.getSummariesToSend()) == 1)
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        
        self.c.setTau(10)
        # hops are too big so 22 should not be included
        self.c.receivedSummaries[22].setHops(100)
        
        expected = sorted([1, 100])
        result = []
        
        for i in self.c.getSummariesToSend():
            result.append(i.getId())
        
        #print sorted(result)
        self.assertTrue(expected == sorted(result))
        
    def test_getReceivedSummaries_shortedHops(self):
        # when there is only myContext
        self.c.setMyContext(self.summary)
        self.assertTrue(len(self.c.getSummariesToSend()) == 1)
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        
        self.c.setTau(10)
        self.c.receivedSummaries[22].setHops(2)
        
        expected = sorted([1, 22, 100])
        result = []
        
        for i in self.c.getSummariesToSend():
            result.append(i.getId())
        
        #print sorted(result)
        self.assertTrue(expected == sorted(result))
        
    def test_resetAllSummaryData(self):
        self.c.resetAllSummarydata()
        self.assertTrue(self.c.getMyContext() is None)
        self.assertTrue(self.c.getGroupContexts() == {})
        self.assertTrue(self.c.getReceivedSummaries() == {})
        
    def test_setTauAndRemoveSummaries(self):
        db3 = {"GroupsEnumerated":3,
              "Group0":100,"Group1":202,"Group2":203,
              }
        summary3 = ContextSummary(33, db3)
        ### SETUP
        self.c.setMyContext(self.summary)
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2, 33:summary3})
        self.c.addGroupDefinition(g)
        self.c.receivedSummaries[22].setHops(100)
        
        self.c.setTauAndRemoveSummaries(10) # We should delete 22
        self.assertTrue(len(self.c.receivedSummaries) == 1)
        
    def test_getGroupSummary(self):
        self.c.setMyContext(self.summary)
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        
        a = self.c.groupContexts[100]
        b = self.c.getGroupSummary(100)
        self.assertFalse(id(a) == id(b))
        self.assertTrue(a == b)
        
    def test_getGroupSummaries(self):
        self.c.setMyContext(self.summary)
        g = GroupDefinition(100)
        self.c.setMyContext(self.summary) # 1
        self.c.setReceivedSummaries({22:self.summary2})
        self.c.addGroupDefinition(g)
        
        a = self.c.getGroupSummaries() 
        b = [self.c.groupContexts[100]]
        self.assertTrue(a,b)
        
        # b = self.c.getGroupSummary(100)
        # self.assertFalse(id(a) == id(b))
        # self.assertTrue(a == b)
        
    def test_setReceivedSummaries_listInput(self):
        inputs = [self.summary, self.summary2]
        self.c.setReceivedSummaries(inputs)
        summaries = self.c.getReceivedSummaries()
        # summaries is a dictionary
        for summary in summaries.values():
            self.assertTrue(summary in inputs)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)