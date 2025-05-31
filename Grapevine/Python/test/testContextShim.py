import unittest
import sys
import copy
sys.path.append("../src")

from contextShim import *
from util.util import *

class TestContextShim(unittest.TestCase):
    def setUp(self):
        self.c = ContextShim()
        
        # SETUP
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":102,"Group2":103,
              "IdsAggregated":5,
              "Id0":10, "Id1":20, "Id2":30, "Id3":40, "Id4":50
              }
        self.summary = ContextSummary(1, db)
        self.s = ContextSummarySerializer()
        
        db1 = {"GroupsEnumerated":3,
              "Group0":100,"Group1":101,"Group2":102
              }
        self.summary1 = ContextSummary(2, db1)
        self.summary1.setTimestamp(time.time())
        time.sleep(0.01)
        db2 = {"GroupsEnumerated":3,
              "Group0":100,"Group1":102,"Group2":103
              }
        self.summary2 = ContextSummary(3, db2)
        self.summary2.setTimestamp(time.time())
        
        self.group = None
        
    def test_getContextBytes(self):
        """
        Set contextHandler for the shim, and the shim will give you
        correct bytes to send
        """
        contextHandler = self.c.getContextHandler()
        contextHandler.setMyContext(self.summary)
        contextHandler.setReceivedSummaries({2:self.summary1, 3:self.summary2})
        self.summary1.setHops(1) # only shorter hops can be included
        self.summary2.setHops(1) # only shorter hops can be included
        
        # 100 is a group, and 1 has group0(100)
        # so addGroupDefinition adds 1 into the member of 100
        g = GroupDefinition(100)
        contextHandler.addGroupDefinition(g)
        self.group = contextHandler.get(100)
        
        numberToSend = contextHandler.getSummariesToSend()
        self.assertEqual(4, len(numberToSend))
        res = self.c.getContextBytes()
        self.assertEqual(448, len(res))
        return res
        
    def test_setprocessContextBytes(self):
        # get the stream buffer
        res = self.test_getContextBytes()
        summaries = self.c.processContextBytes(res)
        expecteds = [self.summary, self.summary2, self.summary1,  self.group]
        hit = 0
        for summary in summaries:
            for expected in expecteds:
                # We can't compare summary and expected one by one
                # as summary has +1 in hops because processContextBytes increases it by 1
                
                #print summary
                #print expected
                if summary.getId() == expected.getId():
                    hit += 1

        self.assertTrue(hit == 4)
        
    def test_sameExceptHops(self):
        summary = copy.deepcopy(self.summary)
        summary.setHops(100)
        self.assertTrue(summary.sameExceptHops(self.summary))
        
if __name__ == "__main__":
    unittest.main(verbosity=2)