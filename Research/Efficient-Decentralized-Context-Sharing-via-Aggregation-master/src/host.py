import sys
import os.path

from util import *
from context import *
from database import *
from buffer import *
from sentHistory import *
#from contextAggregator import *
from demerge import *
from merge import *
from selection import *
from copy import *
from contextsForOneSimulator import *

DEBUG = True

class Host(object):
    def __init__(self, i, neighbors = None): #, analyzer = None):
        # singleton that is shared by all the hosts
        self.contextsDictionary = getContextsForOneSimulator()
        self.id = i
        #self.neighbors = neighbors
        self.neighbors = [] if neighbors is None else neighbors
        #self.resetContexts() # self.contexts 
        self.sampledValue = None
        self.samples = None
        self.sampleTime = 0
        self.drop_failure_count = 0
        self.drop_success_count = 0
        
        self.db = Database()
        self.currentInputDictionary = {}
        self.inputDictionary = {}
        self.outputDictionary = {}
        self.outputBuffer = Buffer()
        self.oldOutputBuffer = Buffer()
        self.sentHistory = SentHistory()
        self.neighborDictionary = {}
        
        self.demerge = Demerge(self.db, self.inputDictionary)
        self.merge = Merge(self.db)
        param = {"outputBuffer":self.outputBuffer, "oldOutputBuffer":self.oldOutputBuffer,
                 "currentInputDictionary":self.currentInputDictionary,
                 "inputDictionary":self.inputDictionary}
        #self.selection = Selection(**param)
        #self.analyzer = analyzer
        #self.sentHistory = SentHistory()
        #######
        
    def __str__(self):
        nullresult = ""
        result = nullresult
        result += "**** Host %d **************************\n" % self.id
        result += "%s" % str(self.db)
        result += "inputDictionary - %s\n" % toStr(self.inputDictionary)
        #result += "currentInputDictionary - %s\n" % toStr(self.currentInputDictionary)
        result += "outputBuffer - %s\n" % self.outputBuffer
        result += "oldOutputBuffer - %s\n" % self.oldOutputBuffer
        result += "outputDictionary - %s\n" % toStr(self.outputDictionary)
        result += "***************************************\n"
        return result
        # return nullresult
        
    def readFromSampleDataFile(self, sampleFile):
        self.sampleFile = sampleFile
        #print
        sampleFile = os.path.abspath(sampleFile)
        assert os.path.exists(sampleFile)
        
        with open(sampleFile) as f:
            #print f
            # line = filter(lambda x: x.startswith(str(self.id)), f.readlines())
            # # TODO
            # # Make it just work
            # #if not len(line): line[0] = 20
            # assert len(line) == 1
            # first, rest = getFirstRest(line[0])
            # assert first == self.id
            #print
            #self.samples = rest
            self.samples = [11, 12, 13]
        
    def sample(self, time = -1):
        try:
            if time == -1:
                res = self.samples[self.sampleTime]
                self.sampleTime += 1
                return res
            else:
                assert len(self.samples) > time
                return self.samples[time]
        except Exception:
            # If anything bad happens, just use the id for the sampling data
            return self.id

    #def resetContexts(self):
        #self.sendContexts = set()
        
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
        
    def getDb(self):
        return self.db
        
    def getNeighbors(self):
        return self.neighbors

    def addToNeighbor(self, n):
        self.neighbors.append(n)

    def deleteNeighbor(self, n):
        """
        remove neighbor 'n' when it's in the neighbors list
        """
        try:
            index = self.neighbors.index(n) # find where is the neighor n
            del self.neighbors[index]
        except ValueError:
            pass

    def setNeighbors(self, n):
        self.neighbors = n
        
    def setNeighborDictionary(self, neighborDictionary):
        self.neighborDictionary = neighborDictionary

    # For Jython interface
    def generateSingleContext(self, value, timeStep = 0):
        return self.generateContext(timeStep, value)

    def generateContext(self, timeStep = 1, sampleValue = None, printFlag = False, s = False):
        """Generate contexts and store them in contexts list
    
        We don't use printFlag now, but it will be used sooner or later for debugging. 
        """

        if sampleValue is not None:
            self.sampledValue = sampleValue
        else:
            self.sampledValue = self.sample(0)

        param = {"id":self.getId(),
                 "value":self.sampledValue,
                 "timeStamp":timeStep,
                 "hopcount":0}
        context = Context(**param)
        # For timestep 0
        if timeStep == 0:
            self.db.singleContexts.add(context)
        else:
            self.inputDictionary = self.currentInputDictionary
            self.currentInputDictionary = {}
            
        # update the db
        demerge = Demerge(self.db, self.inputDictionary)
        self.db = demerge.run()
        #print self.db
    
        #debugging
        # if timeStep >= 1:
        #     print self.db
        #     printDict(self.inputDictionary)
        #     print "----\n"
        
        self.oldOutputBuffer = self.outputBuffer
    
        merge = Merge(self.db)
        self.outputBuffer = merge.run(s)
        
        param = {"outputBuffer":self.outputBuffer, "oldOutputBuffer":self.oldOutputBuffer,
                 "currentInputDictionary":self.currentInputDictionary,
                 "inputDictionary":self.inputDictionary,
                 "sentHistory":self.sentHistory,
                 "neighbors":self.neighbors}
        #print self.inputDictionary
        selection = Selection(**param)
        self.outputDictionary = selection.run(s)
        self.sentHistory.addDictionary(self.outputDictionary)

        # print "Inside host#generateContext host(%d) timestep(%d)" % (self.id, timeStep)
        # print self.outputDictionary

        return self.__str__()
        
    def sendContextsToNeighbor(self, n, printFlag = False):
        #print n
        host = self.neighborDictionary[n]
        contexts = self.outputDictionary[n]
        #print contexts
        host.receiveContexts(self.id, contexts, printFlag)

    def _sendContexts(self, n):
        """
        This method is for ONE Simulation
        """
        contexts = self.outputDictionary[n]
        self.contextsDictionary.sendContexts(self.id, n, contexts)

    def _receiveContexts(self, n):
        sender = n
        contexts = self.contextsDictionary.receiveContexts(n)
        self.receiveContexts(sender, contexts)
        #print self

    def sendContextsToNeighbors(self, dropRate=0.0, printFlag=False):
        assert len(self.neighborDictionary) > 0, "Missing neighborDictionary"
        
        # get neighbor object
        #print printFlag
        #for host, nobject in self.neighborDictionary.items():
        for n in self.neighbors:
            # truefalse() returns true based on the input.
            # We think in terms of droprate, which has (1 - droprate) relationship
            # with the input of truefalse().
            if truefalse(1 - dropRate):
                self.drop_success_count += 1
                self.sendContextsToNeighbor(n, printFlag)
            else:
                self.drop_failure_count += 1
    
    def receiveContexts(self, sender, contexts, printFlag = False):
        assert type(contexts) in [list, set]
        context = increaseHopcount(contexts)
        self.currentInputDictionary[sender] = contexts
            
        if printFlag:
            contextsString = getStringFromList(contexts)
            print "(%d) received Contexts from (%d): %s" % (self.id, sender, contextsString)

    def getContextSizeInOutputDictionary(self, id):
        """
        TODO: The actual size of the context depends on the content representation
        For maximal 500 node -> 500/8 = 63 byte, Double precision data = 8 byte
        = 8 + 63 = 71 byte for one context
        """
        try:
            contexts = self.outputDictionary[id]
            #print contexts
            if contexts:
                return 500/8 + 1 + 8
            else:
                return -1
        except KeyError:
            print self.outputDictionary
            print >>sys.stderr, "ID %d is not in outptuDictionary" % id
            return -1

if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testHost import *

    os.chdir("../test")
    unittest.main(verbosity=2)