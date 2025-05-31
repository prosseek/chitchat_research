import unittest
import sys
import time
sys.path.append("../src")

from datagramContextShim import *

class TestDatagramContextShim(unittest.TestCase):
    def setUp(self):
        ContextHandler.resetContextHandler()
        self.c = DatagramContextShim()
        
        # SETUP
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":102,"Group2":103,
              "IdsAggregated":5,
              "Id0":10, "Id1":20, "Id2":30, "Id3":40, "Id4":50
              }
        self.summary = ContextSummary(1, db)
        #self.s = ContextSummarySerializer()
        
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
        
    def test_getSendPacket(self):
        # SETUP for context summary
        # It starts with getting the context handler
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
        
        lenContextByte = len(self.c.getContextBytes())
        payLoad = "Hello, world"
        result = self.c.getSendPacket(payLoad)
        
        self.assertEqual(4 + len(payLoad) + lenContextByte, len(result))
        return result
        
    def test_processReceivedPacket(self):
        result = self.test_getSendPacket()
        # get 464 bytes, and process the information
        payload, summaries = self.c.processReceivedPacket(result)
        self.assertEqual(payload, "Hello, world")
        # Need to have a routine to compare the two summaries are the same except the hop number
        self.assertTrue(summaries[0].sameExceptHops(self.summary))
        self.assertTrue(summaries[1].sameExceptHops(self.group))
        self.assertTrue(summaries[2].sameExceptHops(self.summary1))
        self.assertTrue(summaries[3].sameExceptHops(self.summary2))
        
    def test_create(self):
        summary = ContextSummary(1)
        summary.put("test value 1", 1)
        summary.put("test value 2", 2)

        handler = ContextHandler.getInstance();
        handler.updateLocalSummary(summary)
        self.assertEqual(66, len(self.c.getContextBytes()))
        
if __name__ == "__main__":
    unittest.main(verbosity=2)