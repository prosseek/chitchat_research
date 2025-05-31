__author__ = 'smcho'

import sys
from pprint import *

class ContextsForOneSimulator(object):
    """
    Singleton for accessing contexts among nodes in ONE Simulator
    """
    def __init__(self):
        self.contexts = {}

    def sendContexts(self, senderNode, receiverNode, contexts):
        if not (senderNode in self.contexts):
            self.contexts[senderNode] = []

        self.contexts[senderNode].append([senderNode, receiverNode, contexts])
        #pprint(self.contexts)

    def receiveContexts(self, senderNode):
        """
        Returns the last context sent to node
        """
        if not (senderNode in self.contexts):
            print >>sys.stderr, "Error! no sender node in contexts"
            return None

        #pprint(self.contexts)
        if self.contexts[senderNode]:
            #print self.contexts[node]
            contexts = self.contexts[senderNode][-1][2] # -1 means the last node assigned, 2 is where the contexts is located
            return contexts
        return None

contextsForOneSimulator = ContextsForOneSimulator()

def getContextsForOneSimulator(): return contextsForOneSimulator

if __name__ == "__main__":
   import unittest
   sys.path.append("../test")
   from testContextsForOneSimulator import *
   unittest.main(verbosity=2)