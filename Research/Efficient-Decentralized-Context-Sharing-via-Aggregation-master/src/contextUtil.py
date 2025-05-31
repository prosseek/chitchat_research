from context import *
from groupContext import *
from util import *
from exactCover import *
from maxCover import *

def maxCover(contexts):
    assert type(contexts) in [set, list]
    
    if not contexts: return contexts
    
    # X = {
    #     'A': [1, 2, 3],
    #     'B': [3, 4],
    #     'C': [4, 5, 6]
    # }
    # make universe
    universe = set()
    X = {}
    contexts = list(contexts) # we need an index, so contexts should be a list
    for i, g in enumerate(contexts):
        #elements = g.getElements()
        elements = [index.getId() for index in g.getElements()]
        #print elements
        X[i] = list(elements)

    #print X

    e = MaxCover()
    res = e.solve(X)
    
    if res is None: return None
    
    result = []
    for i in res:
        result.append(contexts[i])
    
    #printList(result)
    return result

def exactCover(contexts):
    assert type(contexts) in [set, list]
    
    # make universe
    universe = set()
    Y = {}
    contexts = list(contexts) # we need an index, so contexts should be a list
    for i, g in enumerate(contexts):
        elements = g.getElements()
        universe |= elements
        Y[i] = list(elements)
        
    # make X
    X = universe

    e = ExactCover()
    res = e.solve(universe,Y)
    #print res
    
    if res is None: return None
    
    result = []
    for i in res:
        result.append(contexts[i])
    
    #printList(result)
    return result 

# def elemIsInThisGroup(elem, group):
#     assert type(group) is GroupContext
#     e = group.getElements()
#     if elem in e:
#         return True
#     else:
#         return False
# 
# def findGroupThatHasThisElement(elem, groups):
#     assert type(groups) in [set, list]
#     result = set()
#     for g in groups:
#         es = g.getElements()
#         if elem in es:
#             result.add(g)
#     return result
#     
# def groupElementIsInTheseGroups(group, groups):
#     assert type(group) is GroupContext
#     assert type(groups) in [set, list]
#     
#     # Case1: when groups is None, return false
#     # when groups has none, the result should be false
#     if len(groups) == 0: return False
#     
#     dirty = set()
#     
#     elems = group.getElements()
#     for e in elems:
#         gr = findGroupThatHasThisElement(e, groups)
#         
#         # Case2: when there is no group that has element, return false
#         if len(gr) == 0: return False
#         for g in gr:
#             dirty.add(g)
#             
#     return len(groups) == len(dirty)

def removeDuplicate(contexts):
    assert type(contexts) in [list, set]
    if type(contexts) is list:
        result = []
    else:
        result = set()
        
    for c in contexts:
        inResult = False
        for k in result:
            if c == k:
                inResult = True
        if not inResult:
            if type(contexts) is list:
                result.append(c)
            else:
                result.add(c)
                
    return result
    
# def findFirstIndexBiggerThanLength(contexts, length):
#     # assumption: contexts is sorted with length as a key
#     for i, c in enumerate(contexts):
#         #print i, len(c)
#         size = len(c)
#         if size > length:
#             return i
#     return -1

def subtractElements(elem, elemList):
    """Subtract elemeList from elem to check how many
    context is new in elem
    
    elem = [1,2,3,4]
    elemList = [[1,3],[2,5]]
    result = [4]
    """
    l = set()
    for i in elemList:
        if i is not None:
            l |= i.getIdSet()
    m = elem.getIdSet()
    
    return (m - l)
    
# def isNewInfo(output, *p): #prevOutput, aggregated):
#     return len(subtractElements(output, p)) >= 1

def getIds(sent):
    """Returns all the ids in the sent
    """
    result = set()
    if type(sent) in [set, list]:
        for c in sent:
            ids = c.getIdSet()
            result |= ids
    elif type(sent) in [dict]:
        for i,v in sent.items():
            ids = getIds(v)
            result |= ids
    else:
        if type(sent) in [Context, GroupContext]:
            ids = sent.getIds()
            result |= ids
    return result

def isNewInfo(output, *all): #sent, input, currentInput):
    #param = {"output":output, "sent":self.sentHistory.get(host), "input":self.inputDictionary[host], "currentInput":self.currentInputDictionary[host]}
    #print "OUT", output
    ids = set()
    for i in all:
        ids |= getIds(i)
        #print ids
    outputIds = output.getIds()
    #print outputIds
    return len(outputIds - ids) >= 1
    #return False
    
def single(contexts):
    i, a = separateSingleAndGroupContexts(contexts)
    return i
    
def aggregated(contexts):
    i, a = separateSingleAndGroupContexts(contexts)
    #print a
    #printList(a)
    #print len(a)
    # There should be only one aggregated in the contexts
    assert len(a) <= 1
    if len(a) == 1:
        return list(a)[0]
    return None

def issubset(g1, g2):
    """Check if members of g1 is a subset of g2
    """
    # None is subset to everything
    if g1 is None: 
        return True
        
    m1 = set(g1.getIdSet())
    m2 = set(g2.getIdSet())
    # printList(m1)
    # printList(m2)
    return m1 < m2
    
def issuperset(g1, g2):
    """Check if members of g1 is a subset of g2
    """
    # It means when g1 and g2 is None, g1 is superset of g2
    # This logic is necessary as this is used for sending new contexts.
    # When g1 = g2 = None, it means it's the first time to send, and we should return true for 
    # Processing the logic in selection#run()
    if g2 is None: return True
    
    m1 = set(g1.getIdSet())
    m2 = set(g2.getIdSet())
    # printList(m1)
    # printList(m2)
    return m1 > m2

def separateSingleAndGroupContexts(contexts):
    """Given a list comprises of Contexts and GroupContexts, separates them into 
       two sets (individualContexts and GroupContexts set) and return them.

       >>> g1 = [a,b,c]
       >>> gc1 = GroupContext(avg(g1), g1)
       >>> g2 = [a,c,d]
       >>> gc2 = GroupContext(avg(g2), g2)
       >>> 
       >>> contexts = [a,b,gc1,gc2]
       >>> ind, grp = self.i.separateIndividualAndGroupContexts(contexts)
       >>> # check individual contexts
       >>> self.assertTrue(set([a,b]), ind)
       >>> # check group contexts
       >>> self.assertTrue(set([gc1, gc2]), grp)
    """
    individualContexts = set()
    groupContexts = set()
    for c in contexts:
        assert isinstance(c, Context) == True
        if type(c) is Context:
            individualContexts.add(c)
        elif type(c) is GroupContext:
            groupContexts.add(c)
    return individualContexts, groupContexts
    
def isSingle(context):
    return type(context) is Context
    
def isAggregate(context):
    return type(context) is GroupContext
    
def shareMembers(context1, context2):
    memberIds1 = context1.getIdSet()
    memberIds2 = context2.getIdSet()
    #print memberIds1, memberIds2
    result = memberIds1 & memberIds2
    return result
    
def isPrime(context, contextList):
    """Checks if members in context does not share any members in the contexts in contextList
    """
    for c in contextList:
        if shareMembers(context, c): return False
    return True

def getPrime(contextList):
    """Finds all of the prime contexts from contextList
    """
    prime = []
    for c in contextList:
        contextList2 = deepcopy(contextList)
        contextList2.remove(c)
        if isPrime(c, contextList2):
            prime.append(c)
    return prime

def remove(contextList, contextRemoved):
    if type(contextRemoved) in [list, set]:
        for c in contextRemoved:
            contextList = remove(contextList, c)
        return contextList
    else:
        assert type(contextList) in [list]
        result = []
    
        for i in contextList:
            if contextRemoved == i: 
                continue
            result.append(i)
        return result

def subtractFromList(aList, bList):
    """returns a - b
    """
    result = []
    assert type(aList) in [list, set]
    assert type(bList) in [list, set]
    for a in aList:
        if a not in bList:
            result.append(a)

    return result

def substract(superSetGroupContext, subSetGroupContext):
# subtracts from superset GroupContext the ci
# to create Context or GroupContext
    superMembers = superSetGroupContext.getElements()
    superIds = superSetGroupContext.getIdSet()
    
    subIds = subSetGroupContext.getIdSet()
    
    assert superIds.issuperset(superIds)
    ids = superIds - subIds
    members = []
    for i in ids:
        members.append(superSetGroupContext.getContext(i))
        
    if len(members) == 1:
        # Reconstructed context
        context = members[0]
        #print context
        #TODO
        # I make a recontructed context with tau = 10,000
        context.setHopcount(-1)
        return context
    elif len(members) == 0:
        return None
        
    return GroupContext(None, members) 

def findSuperset(ci, c):
    """Given a Context/groupContext ci, and a list of contexts.
    This method returns a list of context whose elements are superset of ci's element.
    This method uses polymorphism in the sense that c can be a list or an element.


    TODO:
      Think and modify: Is it a good idea to return different data type based on the input? 
    """
    assert isinstance(ci, Context)
    #assert type(c) in [set, list]
    if type(c) in [set, list]:
        result = set()
        for i in c:
             res = findSuperset(ci, i)
             if res is not None:
                 result.add(res)
        return result
    else:
        # if c is just a group context
        if type(c) is Context:
            return None # one context cannot be another's super set
        else:
            if ci == c: # ci should be different from c
                return None
        
        idSet = ci.getIdSet()
        groupMemberIdSet = c.getIdSet()
        if groupMemberIdSet.issuperset(idSet):
            return c
        else:
            return None

if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testContextUtil import *

    import os
    os.chdir("../test")
    unittest.main(verbosity=2)