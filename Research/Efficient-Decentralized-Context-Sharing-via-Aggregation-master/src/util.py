import sys
import re
import random

def truefalse(percentage):
    """Returns true or false based on the input.

    Given percentage in double data format, this function
    returns true with the probability given as an input.
    For example, when percentage == 0.1 (10%), this function returns true with the
    probability of 10.

    For seed() method, parameter is not needed.
    http://stackoverflow.com/questions/1703012/what-is-suggested-seed-value-to-use-with-random-seed
    """
    random.seed()
    r = random.random()
    return r < percentage

def printAccuracy(dictionary):
    assert type(dictionary) is dict
    result = ""
    
    totalNumberOfNodes = len(dictionary[1])
    for key, values in dictionary.items():
        average = sum(values.values())/(1.0*totalNumberOfNodes)
        temp = "STEP: %d -> AVG %5.2f%%" % (key, 100.0*(average/totalNumberOfNodes))
        #print temp
        result += (temp + "\n")
    #print result
    return result

def printAccuracyCohorts(dictionary):
    """Print out the cohort information in a dictionary.
       The cohort is in [NUMBER OF COHORTS, THE TOTAL ELEMENTS OF COHORTS] format.

       dictionary is in the format of :
       {1: {0: [0, 0], 1: [0, 0], 2: [0, 0], 3: [0, 0] ...
    """
    #print dictionary
    assert type(dictionary) is dict
    result = ""

    totalNumberOfNodes = len(dictionary[1])
    for key, values in dictionary.items():
        total_number_of_elements = 0
        number = 0
        for node, t in values.items():
            #print node, t
            number += t[0]
            total_number_of_elements += t[1]

        average = total_number_of_elements / number if total_number_of_elements != 0 else 0
        #print average

        temp = "STEP: %d -> COHORTS number(%d), total member size(%d), average member in cohort (%5.2f)" % (key, number, total_number_of_elements, average)
        #print temp
        result += (temp + "\n")
    #print result
    return result

def increaseHopcount(contexts):
    if type(contexts) in [list, set]:
        result = []
        for c in contexts:
            c = increaseHopcount(c)
            result.append(c)
            return result
    else:
        contexts.increaseHopcount()
        return contexts

def getStringFromList(contextList):
    string = ""
    if type(contextList) in [list, set]:
        string += "["
        for c in contextList:
            string += str(c) + ":"
        string = string[0:len(string)-1] + "]"
    else:
        string += str(contextList)
        
    return string 
        
def getFirstRest(l):
    """Separate first item and the rest 
    
    input: "1: 1 2 3 4 5"
    ouptut: 1, [1,2,3,4,5]
    """
    assert type(l) is str
    
    regex = re.compile("^(\d+):\s+((\d+\s*)+)")
    res = regex.search(l.rstrip())
    first = int(res.group(1))
    rest = map(lambda x: int(x), res.group(2).split(' ')) 
    return first, rest

def intersection(g1, g2):
    e1 = g1.getElements()
    e2 = g2.getElements()
    return e1 & e2 #e1.intersection(e2)
    
def union(g1, g2):
    e1 = g1.getElements()
    e2 = g2.getElements()
    return e1 | e2 #e1.union(e2)
    
def diff(g1, g2):
    e1 = g1.getElements()
    e2 = g2.getElements()
    return e1 - e2

def isIn(context, contexts):
    for c in contexts:
        if context == c: return True
    return False
        
def same(contexts1, contexts2):
    """Determine if list c1 and c2 are the same
    """
    #print 'same'
    # 1. if the length of unique elements is different they are different
    s1 = len(set(contexts1))
    s2 = len(set(contexts2))
    l1 = len(contexts1)
    l2 = len(contexts2)
    
    # print "C1", contexts1
    # print "C2", contexts2
    # print "SL", s1, s2, l1, l2
        
    if s1 == s2 == 0: return True
    if l1 != l2 or s1 != s2: return False
    

    # every element in c2 should be in c1
    for c in contexts2:
        if not isIn(c, contexts1): 
            #print c
            #printList(contexts1)
            return False
        
    return True
    # s1 = set(contexts1)
    # s2 = set(contexts2)
    #return s1 == s2
    
def sameDictionary(dict1, dict2):
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    
    if not same(keys1, keys2): return False
    for k1 in keys1:
        value1 = dict1[k1]
        value2 = dict2[k1]
        if not same(keys1, keys2): return False
    return True
    
def printList(groupList):
    print str(len(groupList)) + ":" + toStr(groupList)
    
def printDict(d):
    assert type(d) is dict
    print toStr(d)
        
def removeLast(string, length = 1):
    return string[0:len(string)-length]
    
def toStr(groupList):
    """TODO: not tested, need more tests
    """
    if type(groupList) in [list,set]:
        
        # When the input has getId(), use it for sorting key
        try:
            groupList = sorted(groupList, key=lambda x: x.getId())
        except AttributeError:
            groupList = sorted(groupList)
            
        string = "["
        for c in groupList:
            string += str(c)
        string += "]"
        return string
    elif type(groupList) is dict:
        if not groupList: return ""
        res = "{"
        for i,v in groupList.items():
            res += "%d:%s|" % (i, toStr(v))
            #res += str(v)

        res = removeLast(res) + "}"
        return res
    else:
        raise Exception("Only list or set is supported")
        
def printGroup(group):
    element = group.getElements()
    printList(element)
        
def avg(l):
    sum = 0
    for i in l:
        if type(i) is int:
            sum += i
        else:
            sum += i.value()
    return sum/len(l)
    
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testUtil import *

    unittest.main(verbosity=2)