import sys
import os.path

from util import *
from context import *
from database import *
from buffer import *
from groupContext import *
from contextUtil import *

DEBUG = False

class Merge(object):
    def __init__(self, database = None, tau = 1):
        if database is None:
            database = Database()
        self.database = database
        self.tau = tau
        #return self.run()
        
    def run(self, s = False):
        bf = Buffer()

        assert self.database is not None
        sc = set(self.database.singleContexts)
        pc = set(self.database.primeContexts)

        contexts = set()
        contexts |= set(sc)
        contexts |= set(pc)
        
        # [2013/09/23] added
        # We can add maximum cover Non-prime aggregates from NP
        npc = set(self.database.nonPrimeContexts)
        if npc:
            result = maxCover(npc)
            if result:
                contexts |= set(result)

        #printList(contexts)
        if len(contexts) >= 2:
            g = GroupContext(None, contexts)
        else:
            g = None
        #print g.value()
        singleContexts = []

        for i in sc:
            if s:
                # For single case, just appends all the single context no matter what
                singleContexts.append(i)
            else:
                # [2013/09/09] bug found
                # i.hopcout is (-1) when it is demerged.
                # it should not be sent outside.
                if i.hopcount < self.tau and i.hopcount >= 0:
                    singleContexts.append(i)
        # self.aggregatedContext = set()
        # self.singleContexts = set()
        if not s:
            # no aggregates in single context case
            bf.aggregatedContext = g
        bf.singleContexts = singleContexts
            
        return bf
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testMerge import *

    os.chdir("../test")
    unittest.main(verbosity=2)