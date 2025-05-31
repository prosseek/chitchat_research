import sys
import os.path

from util import *
from context import *
from contextUtil import *
from buffer import *
from database import *

DEBUG = False

class Demerge(object):
    def __init__(self, database = None, inputDictionary = None):
        if database is None:
            database = set()
        if inputDictionary is None:
            inputDictionary = {}
        
        self.database = database
        self.inputDictionary = inputDictionary
        
    def run(self):
        sc = self.database.singleContexts
        pc = self.database.primeContexts
        contexts = set(sc).union(set(pc))

        for host, cs in self.inputDictionary.items():
            contexts |= set(cs)

        sc,pc,npc = self.demerge(contexts)
        # print sc,pc,npc
        db = Database()
        db.singleContexts = sc
        db.primeContexts = pc
        db.nonPrimeContexts = npc
        return db
        
    def demerge(self, contexts):
        singles, groups = separateSingleAndGroupContexts(contexts)
        usedSingles = []
        singles = list(singles)
        groups = list(groups)
        # groups are sorted by the number of elements
        groups = sorted(groups, key = len)

        index = 0
        size = len(groups)
        
        while (index < size or len(singles) > 0):
            if len(singles): 
                ci = singles.pop()
                usedSingles.append(ci)
                #singles = remove(singles, ci) # I think this is redundunt code
            #elif len(groups):
            else:
                #ci = groups.pop(index)
                #groups.insert(index, ci)
                ci = groups[index]
                
            # find contexts that has ci in it
            supersetList = findSuperset(ci, groups)
            
            if supersetList:
                index = 0 # reset the index
                newlyCreatedAggregate = []
                for superSet in supersetList:
                    a = substract(superSet, ci)
                    if a is None: # superSet == ci
                        #raise Exception("substraction result is None: superSet == ci")
                        pass
                    elif len(a) == 1:
                        singles.append(a)
                        singles = list(set(singles)) # make it unique
                        #index = 0 # ??? Think about this
                    else:
                        newlyCreatedAggregate.append(a)
                        #groups.append(ci)
                        
                groups = remove(groups, supersetList) # remove all the superList that is broken
                groups = groups + newlyCreatedAggregate # add all the newly created ones
                
                groups = removeDuplicate(groups) # Maybe redundunt
                groups = sorted(groups, key = len) # sort the contexts list
                size = len(groups)
            else:
                # No superset, so get the next one
                if isAggregate(ci):
                    index += 1
                
        sc = usedSingles

        pc = getPrime(groups)
        npc = subtractFromList(groups, pc)
        
        cp = maxCover(npc)
        npc = subtractFromList(npc, cp)
        pc.extend(cp)

        #if cp is not None:
        #    groups = cp
        #
        #groups = list(groups)
        #
        #for ci in groups:
        #    groups = remove(groups, ci) # Without this isPrime always returns false
        #    if isPrime(ci, groups):
        #        pc.append(ci)
        #    else:
        #        npc.append(ci)
        #    groups.append(ci)
        #
        return sc,pc,npc
            
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testDemerge import *

    os.chdir("../test")
    unittest.main(verbosity=2)