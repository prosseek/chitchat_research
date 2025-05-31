from groupDefinition import *
from groupContextSummary import *
from util.util import *

DEFAULT_TAU = 3

class ContextHandler(object):
    """
    It's a singleton, so it should be invoked with ConstextHandler.getInstance()
    """
    singleton = None
    
    def __init__(self, tau = None):
        self.myContext = None
        self.groupDefinitions = {} # id -> GroupDefinition
        # different from Evan's: make it plural
        self.groupContexts = {} # id -> GroupContextSummary
        self.receivedSummaries = {}
        self.tau = DEFAULT_TAU if tau is None else tau
        
    @staticmethod
    def resetContextHandler():
        ContextHandler.singleton = None
        
    @staticmethod
    def getInstance():
        if ContextHandler.singleton is None:
            ContextHandler.singleton = ContextHandler()
        return ContextHandler.singleton
        
    def setTau(self, newTau):
        self.tau = newTau
    
    def getTau(self):
        return self.tau
        
    def setMyContext(self, summary):
        #print type(summary)
        assert (type(summary) is ContextSummary or summary is None)
        self.myContext = summary
    
    def getMyContext(self):
        return self.myContext
        
    def setReceivedSummaries(self, summaries):
        # Summary should be dict type
        if type(summaries) is dict:
            self.receivedSummaries = summaries
        elif type(summaries) is list:
            self.receivedSummaries = {}
            for summary in summaries:
                uid = summary.getId()
                self.receivedSummaries[uid] = summary
        else:
            raise Exception("Only list or dict is allowed for input")
        return self.receivedSummaries
    
    def getReceivedSummaries(self):
        return self.receivedSummaries
        
    def resetGroupDefinitions(self):
        self.groupDefinitions = {}
        
    def getGroupContext(self, gId):
        if gId in self.groupContexts:
            return self.groupContexts[gId]
        else:
            return None
    
    def setGroupContexts(self, groupContexts):
        assert (type(groupContexts) is dict)
        self.groupContexts = groupContexts
        return self.groupContexts
        
    def getGroupContexts(self):
        return self.groupContexts
            
    def getGroupDefinition(self, gId):
        if gId in self.groupDefinitions:
            return self.groupDefinitions[gId]
        else:
            return None
    
    def performGroupFormations(self, groupDefinitions, summaries):
        """
        groupDefinitions has all the group information.
        summaries has the incoming summaries as a list
        
        1. for all groupDefiniton, find 
        """
        #print summaries
        for gd in groupDefinitions.values():
            gid = gd.getId()
            groupSummary = self.groupContexts[gid]
            #print groupSummary
            
            for summary in summaries:
                uid = summary.getId()
                #print uid
                if uid == gid:
                    #print gid
                    gd.handleGroupSummary(groupSummary, summary)
                    # ????
                    # Why remove summary
                    del summary
                else:
                    #print groupSummary
                    #print summary
                    gd.handleContextSummary(groupSummary, summary)
                    #print groupSummary
    
    def setupGroupDefinition(self, groupDefinition):
        """
        Given groupDefinition
        1. create GroupContextSummary from the gid in the groupDefintion
        2. setup groupContexts/groupDefinitions 
        """
        gId = groupDefinition.getId()
        groupSummary = GroupContextSummary(gId)
        #print >> sys.stderr, "%d - %s" % (gId, groupSummary)
        self.groupContexts[gId] = groupSummary
        self.groupDefinitions[gId] = groupDefinition
                
    def addGroupDefinition(self, groupDefinition):
        self.setupGroupDefinition(groupDefinition)
        gId = groupDefinition.getId()
        # You have to get the group summary from groupContexts dictionary
        groupSummary = self.groupContexts[gId]

        myContext = self.getMyContext()
        if myContext is not None:
            groupDefinition.handleContextSummary(groupSummary, myContext)
            
        self.performGroupFormations(self.groupDefinitions, self.receivedSummaries.values())
        
    def updateLocalSummary(self, summary):
        self.myContext = summary.getWireCopy()
        
        for groupDefinition in self.groupDefinitions.values():
            gId = groupDefinition.getId()    
            groupSummary = self.groupContexts[gId]    
            groupDefinition.handleContextSummary(groupSummary, self.myContext)

    def removeLocalSummary(self):
        self.myContext = None
        
    def handleIncomingSummaries(self, summaries):
        summariesToPut = []
        for summary in summaries:
            #print summary
            uid = summary.getId()
            
            # Bump hop counter
            summary.incrementHops()
            
            # Is received summary local?
            if (self.myContext is not None and self.myContext.getId() == uid):
                continue
            
            # Do we already have the best version of this summary?
            if uid in self.receivedSummaries:
                #print uid
                #print summary.getTau()
                #print self.receivedSummaries[uid].getTau()
                existing = self.receivedSummaries[uid]
                if summary.getTimestamp() < existing.getTimestamp() \
                    or (summary.getTimestamp() == existing.getTimestamp() and summary.getHops() >= existing.getHops()):
                    continue # skip when time stamp is older (smaller) or tau is longer (bigger)
            #print summary
            # dprint(summary)
            # if type(summary) is GroupContextSummary: dprint('group')
            # else: dprint('non group')
            summariesToPut.append(summary)
        
        #print summariesToPut
        #for s in summariesToPut:
        #    print s.getId()
        ### ???
        # Why do we need this?
        #dprint(summariesToPut)
        self.performGroupFormations(self.groupDefinitions, summariesToPut);
        
        #print summariesToPut
        # Evan's code uses notification, but not this
        for summaryToPut in summariesToPut:
            self.receivedSummaries[summaryToPut.getId()] = summaryToPut
    
    def get(self, uid):
        # returns myContext from ID
        if self.myContext is not None and self.myContext.getId() == uid:
            return self.myContext.getCopy()
        if uid in self.groupContexts:
            return self.groupContexts[uid].getCopy()
        if uid in self.receivedSummaries:
            return self.receivedSummaries[uid].getCopy()
        
        return None
    
    # # ???
    # def getWithKey(self, uid, key):
    #     summary = self.get(uid)
    #     if summary is None: return None
    #     return summary[uid]
        
    def getSummariesToSend(self):
        summaries = []
        if self.getMyContext() is not None:
            summaries.append(self.myContext)
        
        for groupSummary in self.groupContexts.values():
            summaries.append(groupSummary.getWireCopy())
            
        for summary in self.receivedSummaries.values():
            #print summary.getHops()
            #print self.tau
            if summary.getHops() < self.tau:
                summaries.append(summary)
                
        return summaries
        
    def resetAllSummarydata(self):
        self.setMyContext(None)
        self.resetGroupDefinitions()
        self.setGroupContexts({})
        self.setReceivedSummaries({})
        
    def setTauAndRemoveSummaries(self, tau):
        self.setTau(tau)
        for summary in self.receivedSummaries.values():
            if summary.getHops() >= tau:
                del self.receivedSummaries[summary.getId()]
                
    def getGroupSummary(self, gid):
        groupSummary = self.groupContexts[gid]
        if groupSummary is not None:
            return groupSummary.getGroupCopy()
        return None
        
    def getGroupSummaries(self):
        summaries = []
        for summary in self.groupContexts.values():
            summaries.append(summary)
            
        return summaries
    
if __name__ == "__main__":
    import sys
    sys.path.append("../test")
    from testContextHandler import *
    
    unittest.main(verbosity=2)