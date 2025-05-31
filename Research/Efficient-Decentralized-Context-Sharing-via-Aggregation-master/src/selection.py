import sys
import os.path

from util import *
from context import *
from database import *
from buffer import *
from groupContext import *
from contextUtil import *
from sentHistory import *

DEBUG = False

class Selection(object):
    def __init__(self, 
            inputDictionary = None, currentInputDictionary = None, 
            outputBuffer = None, oldOutputBuffer = None, 
            sentHistory = None, neighbors = None):
        
        self.inputDictionary = inputDictionary
        self.currentInputDictionary = currentInputDictionary
        self.outputBuffer = outputBuffer
        self.oldOutputBuffer = oldOutputBuffer
        self.sentHistory = sentHistory
        if self.sentHistory is None:
            self.sentHistory = SentHistory()
            
        self.neighbors = neighbors
        if neighbors is None:
            self.neighbors = []
        
    def run(self, s = False):
        # s is for single aggregation case
        
        #print self.inputDictionary
        outDictionary = {}
        output = self.outputBuffer.aggregatedContext
        outputSingles = self.outputBuffer.singleContexts
        oldOutputSingles = self.oldOutputBuffer.singleContexts
        prev = self.oldOutputBuffer.aggregatedContext
        
        ## TODO
        ## single output to aggregated case should be tested more
        newOutputSingles = set(outputSingles) - set(oldOutputSingles)
        
        assert type(output) in [type(None), GroupContext], "wrong type %s" % type(output)
        assert type(prev) in [type(None), GroupContext], "wrong type %s" % type(output)
        
        if s: # single case
            for host in self.neighbors:
                newInformation = newOutputSingles

                if host in self.inputDictionary:
                    contexts = self.inputDictionary[host]
                else:
                    contexts = []

                if host in self.currentInputDictionary:
                    currentContexts = self.currentInputDictionary[host]
                else:
                    currentContexts = []
                    
                oldInformation =  contexts + list(self.sentHistory[host]) # + self.currentInputDictionary[host] 
                newInformation = newInformation - set(oldInformation)
                outDictionary[host] = list(newInformation)
                #self.sentHistory.add(host, set(newInformation))
        else:
            if issuperset(output, prev):
                # For the first time sending, selection just selects all the nodes to my individual context
                if output is None and prev is None:
                    for n in self.neighbors:
                        outDictionary[n] = newOutputSingles
                else:
                    for host in self.neighbors:
                        #print host
                        if host in self.inputDictionary:
                            contexts = self.inputDictionary[host]
                        else:
                            contexts = []

                        if host in self.currentInputDictionary:
                            currentContexts = self.currentInputDictionary[host]
                        else:
                            currentContexts = []
                
                        #printList(contexts)
                        agFromInput = aggregated(contexts)
                        #print agFromInput
                        agFromCurrentInput = aggregated(currentContexts)
                        sg = single(contexts)
                        currentAg = single(currentContexts)
                
                        resultContexts = []
                
                        #if isNewInfo(output, prev, agFromInput, agFromCurrentInput):
                        if host in self.inputDictionary:
                            i = self.inputDictionary[host]
                        else:
                            i = []
                        if host in self.currentInputDictionary:
                            c = self.currentInputDictionary[host]
                        else:
                            c = []
                        
                        #param = {"output":output, "sent":, "input":i, "currentInput":c}
                        # print "***"
                        # print output
                        # printList(self.sentHistory.get(host))
                        # printList(i)
                        # print "???"
                    
                        #print self.sentHistory
                        if isNewInfo(output, *[self.sentHistory.get(host), prev, i, c]):
                            resultContexts.append(output)
                    
                        #print resultContexts
                        for c in newOutputSingles:
                        #for c in outputSingles:
                            #print c
                            #print outputSingles
                            if not isIn(c, sg) and not self.sentHistory.sent(host, c):
                                resultContexts.append(c)
                
                        #print resultContexts
                        outDictionary[host] = resultContexts
        
        #print len(outDictionary['h1'])
        #print outDictionary
        return outDictionary
        
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testSelection import *

    os.chdir("../test")
    unittest.main(verbosity=2)