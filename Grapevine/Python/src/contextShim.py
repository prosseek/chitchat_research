from contextSummarySerializer import *
from contextHandler import *

class ContextShim(object):
    def __init__(self):
        self.contextHandler = ContextHandler.getInstance()
        self.serializer =  ContextSummarySerializer()
        
    def getContextHandler(self):
        return self.contextHandler
        
    def getContextBytes(self):
        summaries = self.contextHandler.getSummariesToSend()
        self.serializer.clearBuffer()
        result = self.serializer.writeSummaries(summaries)
        return result
        
    def processContextBytes(self, buffer):
        """
        When it processes ContextBytes, it uses handleIncomingSummaries,
        it causes to increment hops by 1
        
        Traceback (most recent call last):
          method test_setprocessContextBytes in testContextShim.py at line 61
            summaries = self.c.processContextBytes(res)
          method processContextBytes in testContextShim.py at line 20
            self.contextHandler.handleIncomingSummaries(summaries)
          method handleIncomingSummaries in testContextShim.py at line 150
            summary.incrementHops()
          method incrementHops in testContextShim.py at line 64
            raise Exception("WHY???")
        """
        summaries = self.serializer.readSummaries(buffer)
        self.contextHandler.handleIncomingSummaries(summaries)
        return summaries
    
if __name__ == "__main__":
    import sys
    sys.path.append("../test")
    from testContextShim import *
    unittest.main(verbosity=2)