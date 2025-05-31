import unittest
import sys
sys.path.append("../src")

from contextSummarySerializer import *
from contextSummary import *

class TestContextSummarySerializer(unittest.TestCase):
    def setUp(self):
        db = {"GroupsEnumerated":3,
              "Group0":100,"Group1":102,"Group2":103,
              "IdsAggregated":5,
              "Id0":10, "Id1":20, "Id2":30, "Id3":40, "Id4":50
              }
        self.summary = ContextSummary(1, db)
        self.s = ContextSummarySerializer()
        
        db1 = {"GroupsEnumerated":3,
              "Group0":0,"Group1":1,"Group2":2
              }
        self.summary1 = ContextSummary(2, db1)
        self.summary1.setTimestamp(time.time())
        time.sleep(0.01)
        db2 = {"GroupsEnumerated":3,
              "Group0":0,"Group1":1,"Group2":2
              }
        self.summary2 = ContextSummary(3, db2)
        self.summary2.setTimestamp(time.time())
        
    def test_writeObjectData(self):
        self.s.writeSummary(self.summary)
        # You can't compare the size alone because of the timestamp differences.
        #expected = "[0x1] ... "
        # the self.summary has total of 123 bytes
        self.assertEqual(168, self.s.size())
        
    def test_readObjectData(self):
        self.s.writeSummary(self.summary)
        summary = self.s.readSummary() # serializedData)
        #print summary.timestamp, type(summary.timestamp)
        # print summary
        # print self.summary
        # print type(summary) # returned is group summary
        # print type(self.summary)
        self.assertTrue(summary == self.summary)
        
    def test_writeSummaries(self):
        ### SETUP
        self.s.writeSummaries([self.summary1, self.summary2])
        self.assertEqual(len(self.s.result), 184) #<-- two summaries summarizes up to 182
        #print summary
        # http://stackoverflow.com/questions/12871775/python-compress-ascii-string
        # import zlib
        # comp = zlib.compress(self.s.result)
        # print len(comp) # 73
        # print len(zlib.decompress(comp)) # 182
        
    def test_readSummaries(self):
        expected = [self.summary1, self.summary2]
        res = self.s.writeSummaries(expected)
        #print len(res)
        # result = []
        result = self.s.readSummaries() # res)
        for i in range(len(result)):
            self.assertEqual(result[i], expected[i])
            
    def test_readSummaries_from_buffer(self):
        expected = [self.summary1, self.summary2]
        res = self.s.writeSummaries(expected)
        
        # Modify the stream data
        l = list(res)
        l[1] = '\x05' # Modified the uid of the first summary
        res = "".join(l)
        result = self.s.readSummaries(res) # res)
        
        # modify the summary
        self.summary1.setId(5)
        for i in range(len(result)):
            # print result[i]
            # print expected[i]
            self.assertEqual(result[i], expected[i])
            
    def test_clearBuffer(self):
        expected = [self.summary1, self.summary2]
        res = self.s.writeSummaries(expected)
        self.assertTrue(self.s.getBuffer() != "")
        self.s.clearBuffer() # <--
        self.assertTrue(self.s.getBuffer() == "")
        
if __name__ == "__main__":
    unittest.main(verbosity=2)