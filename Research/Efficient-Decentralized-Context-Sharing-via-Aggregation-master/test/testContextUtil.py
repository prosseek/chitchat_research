import unittest
import sys

sys.path.append("../src")

from contextUtil import *
from context import *
from groupContext import *
from util import *

a = Context(1, 10)
b = Context(2, 20)
c = Context(3, 30)
d = Context(4, 40)
e = Context(5, 50)
f = Context(6, 60)
k = Context(100, 323)

class TestContextUtil(unittest.TestCase):
    def setUp(self):
        pass

    def test_subtractFromList(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [b,c])
        g3 = GroupContext(None, [c,d])
        g4 = GroupContext(None, [d,e])

        aa = [g1,g2,g3]
        bb = [g3]
        result = subtractFromList(aa,bb)
        self.assertTrue(same(result, [g1,g2]))

        bb = [g4]
        result = subtractFromList(aa,bb)
        self.assertTrue(same(result, aa))

        bb = deepcopy(aa)
        result = subtractFromList(aa,bb)
        #print result
        self.assertTrue(result == [])

    def test_getPrime1(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [b,c])
        g3 = GroupContext(None, [c,d])
        g4 = GroupContext(None, [d,e])
        result = getPrime([g1,g2,g3,g4])
        self.assertTrue(result == [])

    def test_getPrime2(self):
        g1 = GroupContext(None, [a,b])
        g3 = GroupContext(None, [c,d])
        g4 = GroupContext(None, [d,e])
        result = getPrime([g1,g3,g4])
        #print result
        self.assertTrue(same(result, [g1]))

    def test_getPrime3(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [k,f])
        g3 = GroupContext(None, [b,c])
        g4 = GroupContext(None, [d,e])
        result = getPrime([g1,g2,g3,g4])
        #print result
        self.assertTrue(same(result, [g2,g4]))

    def test_maximumCover1(self):
        # 1:[<2(97)(99)>]
        a1 = Context(1, 10)
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        a5 = Context(5, 10)
        a6 = Context(6, 10)
        a7 = Context(7, 10)
        a8 = Context(8, 10)
        
        g12 = GroupContext(None, [a1, a2])
        g234 = GroupContext(None, [a2, a3, a4])
        g3458 = GroupContext(None, [a3, a4, a5, a8])
        g567 = GroupContext(None, [a5, a6, a7])
        g78 = GroupContext(None, [a7, a8])
        
        result = maxCover([g12, g234, g3458, g567, g78])
        expected1 = [g3458, g12]
        expected2 = [g234, g567]
        # b = Context(99, 20)
        # g = GroupContext(None, [a,b])
        # result = exactCover([g])
        # printList(expected)
        # printList(result)
        self.assertTrue(same(result, expected1) or same(result, expected2))
        
    def test_maximuCover2(self):
        result = maxCover([])
        self.assertTrue(result == [])
    
    # def test_groupElementIsInTheseGroupsDebugging(self):
    #     # c  :  <2(1)(4)>
    #     # cp : [<2(4)(7)>]
    #     a1 = Context(1, 10)
    #     a4 = Context(4, 10)
    #     a7 = Context(7, 20)
    #     g14 = GroupContext(None, [a1, a4])
    #     g47 = GroupContext(None, [a4, a7])
    #     self.assertFalse(groupElementIsInTheseGroups(g14, [g47]))
    
    def test_exactCover1(self):
        # 1:[<2(97)(99)>]
        a = Context(97, 10)
        b = Context(99, 20)
        g = GroupContext(None, [a,b])
        result = exactCover([g])
        self.assertTrue(same(result, [g]))
        
    def test_exactCover2(self):
        a1 = Context(1, 10)
        a4 = Context(4, 10)
        a7 = Context(7, 20)
        
        g1 = GroupContext(None, [a1, a4])
        g2 = GroupContext(None, [a4, a7])
        
        result = exactCover([g1, g2])
        #print result
        self.assertTrue(result is None)
        
    def test_exactCover3(self):
        # [<2(3)(6)><2(6)(8)><2(2)(8)><2(2)(3)>]
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a6 = Context(6, 20)
        a8 = Context(8, 20)
        
        g36 = GroupContext(None, [a3, a6])
        g68 = GroupContext(None, [a6, a8])
        g28 = GroupContext(None, [a2, a8])
        g23 = GroupContext(None, [a2, a3])
        
        result = exactCover([g23, g28, g36, g68])
        #printList(result)
        self.assertTrue(same(result, [g28, g36]) or same(result, [g23, g68]))
        
    def test_exactCover4(self):
        # [123/345/124] all of them are NP
        a1 = Context(1, 10)
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        
        g123 = GroupContext(None, [a1, a2, a3])
        g34 = GroupContext(None, [a3, a4])
        g124 = GroupContext(None, [a1, a2, a4])
        
        v = [g123, g34, g124]
        result = exactCover(v)
        self.assertTrue(result is None)
        
    def test_exactCover5(self):
        # [123/345/124] all of them are NP
        a1 = Context(1, 10)
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        
        g12 = GroupContext(None, [a1, a2])
        g34 = GroupContext(None, [a3, a4])
        g23 = GroupContext(None, [a2, a3])
        
        expected = [g12, g34]
        v = [g12, g34, g23]
        result = exactCover(v)
        #printList(result)
        self.assertTrue(same(result, expected))
        
    def test_exactCover6(self):
        # [<2(3)(6)><2(6)(8)><2(2)(8)><2(2)(3)>]
        a2 = Context(2, 10)
        a3 = Context(3, 10)
        a4 = Context(4, 10)
        a5 = Context(5, 10)
        a6 = Context(6, 20)
        a7 = Context(7, 20)
        
        g234 = GroupContext(None, [a2, a3, a4])
        g456 = GroupContext(None, [a4, a5, a6])
        g567 = GroupContext(None, [a5, a6, a7])
        
        result = exactCover([g234, g456, g567])
        #printList(result)
        self.assertTrue(same(result, [g234, g567]))
    #     
    # def test_groupElementIsInTheseGroups1(self):
    #     g1 = GroupContext(None, [a,b])
    #     g2 = GroupContext(None, [c,d])
    #     g3 = GroupContext(None, [e,f])
    #     g4 = GroupContext(None, [c,e])
    #     
    #     # a/b : (c/d) + (e/f) -> False
    #     result = groupElementIsInTheseGroups(g1, [g2, g3])
    #     self.assertFalse(result)
    #     
    #     # c/e : (c/d) + (e/f) -> c is in the first, and e is in the second -> True
    #     result = groupElementIsInTheseGroups(g4, [g2, g3])
    #     self.assertTrue(result)
    #     
    #     # c/e : (a/b) + (e/f) -> a/b doesn't contain the element in c/e -> False
    #     result = groupElementIsInTheseGroups(g4, [g1, g3])
    #     self.assertFalse(result)
    #     
    #     
    # def test_groupElementIsInTheseGroups2(self):
    #     g1 = GroupContext(None, [a,b])
    #     g2 = GroupContext(None, [c,d])
    #     g3 = GroupContext(None, [e,f])
    #     g4 = GroupContext(None, [c,e])
    #     
    #     # a/b : (c/d) + (e/f) -> False
    #     result = groupElementIsInTheseGroups(g1, [])
    #     self.assertFalse(result)
    #     
    # def test_findGroupThatHasThisElement(self):
    #     elem = a
    #     g1 = GroupContext(None, [a,b])
    #     g2 = GroupContext(None, [c,d])
    #     g3 = GroupContext(None, [e,f])
    #     g4 = GroupContext(None, [a,b,c,d])
    #     
    #     result = findGroupThatHasThisElement(elem, [g1, g2, g3])
    #     self.assertTrue(same(result, [g1]))
    #     
    #     result = findGroupThatHasThisElement(elem, [g1, g2, g3, g4])
    #     self.assertTrue(same(result, [g1, g4]))
    #     
    #     result = findGroupThatHasThisElement(elem, [g2, g3])
    #     self.assertTrue(same(result, []))
    #     #self.assertTrue(result)
    #     
    #     #result = findGroupThatHasThisElement(elem, [g3, g2])
    #     #self.assertFalse(result)
    #     
    # def test_findGroupThatHasThisElement2(self):
    #     elem = a
    #     
    #     result = findGroupThatHasThisElement(elem, [])
    #     self.assertTrue(same(result, []))
    #     
    # def test_elemIsInThisGroup(self):
    #     elem = a
    #     g1 = GroupContext(None, [a,b])
    #     g2 = GroupContext(None, [c,d])
    #     
    #     result = elemIsInThisGroup(elem, g1)
    #     self.assertTrue(result)
    #     
    #     result = elemIsInThisGroup(elem, g2)
    #     self.assertFalse(result)
    #     
    def test_removeRedundancy(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [c,d])
        g3 = GroupContext(None, [b,c])
        
        result = exactCover([g1, g2, g3])
        expect = [g1, g2]
        self.assertTrue(same(result, expect))
        
    def test_removeDuplicate(self):
        g1 = GroupContext(None, [a,b,c])
        g2 = GroupContext(None, [a,b,c])
        g3 = GroupContext(None, [a,b])
        #print g1 == g2
        res = removeDuplicate([g1, g2, g3])
        expected = [g2, g3]
        self.assertTrue(same(res, expected))
        
    # def test_findFirstIndexBiggerThanLength(self):
    #     g2_1 = GroupContext(None, [a,b])
    #     g2_2 = GroupContext(None, [a,c])
    #     g3_1 = GroupContext(None, [a,c,d])
    #     g3_2 = GroupContext(None, [a,b,c])
    #     g4_1 = GroupContext(None, [a,c,d,e])
    #     g4_2 = GroupContext(None, [a,b,c,d])
    #     g5 = GroupContext(None, [a,b,c,d,e])
    #     
    #     contexts = [g5, g2_1, g2_2, g3_1, g3_2, g4_1, g4_2]
    #     contexts = sorted(contexts, key=len)
    #     
    #     length = 4
    #     result = findFirstIndexBiggerThanLength(contexts, length)
    #     expected = 6 # length 5 starts at the index 6 
    #     self.assertTrue(result == expected)
    #     
    #     length = 2
    #     result = findFirstIndexBiggerThanLength(contexts, length)
    #     expected = 2 # The length 3 starts at index 2
    #     self.assertTrue(result == expected)
    #     
    #     length = 100
    #     result = findFirstIndexBiggerThanLength(contexts, length)
    #     expected = -1
    #     self.assertTrue(result == expected)
        
    def test_isSingle(self):
        self.assertTrue(isSingle(a))
    
    def test_isAggregate(self):
        g = GroupContext(None, [a,b,c])
        self.assertTrue(isAggregate(g))
        
    def test_subtractElements1(self):
        output = GroupContext(None, [a,b,c,d])
        prevOutput = GroupContext(None, [a,e])
        aggregated = None
        
        result = subtractElements(output, [aggregated, prevOutput])
        expected = [2,3,4]
        self.assertTrue(same(expected, result))
        
    def test_getIds1(self):
        res = getIds(a)
        result = list(res)[0]
        self.assertTrue(result == 1)
    
    def test_getIds2(self):
        res = getIds([a,b,c])
        result = list(res)
        self.assertTrue(same(result, [1,2,3]))
        
    def test_getIds3(self):
        g = GroupContext(None, [d,e,f])
        res = getIds({'a':a, 'b':b, 'c':c, 'g':g})
        result = list(res)
        self.assertTrue(same(result, [1,2,3,4,5,6]))
        
    def test_subtractElements2(self):
        output = GroupContext(None, [a,b,c,d])
        prevOutput = GroupContext(None, [a,e])
        aggregated = GroupContext(None, [b,c])
        
        result = subtractElements(output, [aggregated, prevOutput])
        expected = [4]
        self.assertTrue(same(expected, result))
    
    def test_isNewInfo(self):
        output = GroupContext(None, [a,b,c,d])
        prevOutput = GroupContext(None, [a,e])
        aggregated = GroupContext(None, [b,c])
        aggregated2 = None
        # We have result as new
        result = isNewInfo(output, prevOutput, aggregated, aggregated2)
        self.assertTrue(result)
        
    def test_isNewInfo2(self):
        output = GroupContext(None, [a,b,c,d,e,f])
        prevOutput = GroupContext(None, [a,b])
        aggregated = GroupContext(None, [c,d])
        aggregated2 = GroupContext(None, [e,f])
        # We have result as new
        result = isNewInfo(output, prevOutput, aggregated, aggregated2)
        self.assertFalse(result)
        
    def test_isNewInfo3(self):
        output = GroupContext(None, [a,b,c,d,e,f])
        x = GroupContext(None, [a,b])
        y = GroupContext(None, [c,d])
        z = GroupContext(None, [e,f])
        # We have result as new
        result = isNewInfo(output, [x,y,z], {"z":z})
        self.assertFalse(result)
        
    def test_isNewInfo4(self):
        output = GroupContext(None, [a,b,c,d,e,f])
        x = GroupContext(None, [a,b])
        y = GroupContext(None, [d,k])
        z = GroupContext(None, [e,f])
        # We have result as new
        result = isNewInfo(output, [x,y,z], {"z":z})
        self.assertTrue(result)
    
    def test_single(self):
        g1 = [a,b]
        gc1 = GroupContext(None, g1)
        r = single([gc1, c,d,e])
        expected = [c,d,e]
        self.assertTrue(same(expected, r))
        
    def test_aggregated(self):
        g1 = [a,b]
        gc1 = GroupContext(None, g1)
        r = aggregated([gc1, c,d,e])
        expected = gc1
        #print r
        self.assertTrue(expected == r)
        
    def test_subset1(self):
        g1 = [a,b]
        gc1 = GroupContext(None, g1)
        g2 = [a,b,c]
        gc2 = GroupContext(None, g2)
        self.assertTrue(issubset(gc1, gc2))
        
        gc1 = None
        self.assertTrue(issubset(gc1, gc2))
        
    def test_subset2(self):
        g1 = [a,b]
        gc1 = GroupContext(None, g1)
        g2 = [a,b]
        gc2 = GroupContext(None, g2)
        self.assertFalse(issubset(gc1, gc2))
        
    def test_superset1(self):
        g1 = [a,b]
        gc1 = GroupContext(None, g1)
        g2 = [a,b,c]
        gc2 = GroupContext(None, g2)
        self.assertTrue(issuperset(gc2, gc1))
        
        gc2 = None
        self.assertTrue(issuperset(gc1, gc2))
        
    def test_superset2(self):
        g1 = [a,b,c]
        gc1 = GroupContext(None, g1)
        g2 = [a,b,c]
        gc2 = GroupContext(None, g2)
        self.assertFalse(issuperset(gc2, gc1))
        
    def test_separateSingleAndGroupContexts(self):
        g1 = [a,b,c]
        gc1 = GroupContext(None, g1)
        g2 = [a,c,d]
        gc2 = GroupContext(None, g2)
    
        contexts = [a,b,gc1,gc2]
        ind, grp = separateSingleAndGroupContexts(contexts)
        # check individual contexts
        self.assertTrue(set([a,b]), ind)
        # check group contexts
        self.assertTrue(set([gc1, gc2]), grp)
            
    def test_shareMembers(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [c,d])
        
        result = shareMembers(g1, g2)
        expected = set([])
        self.assertTrue(result == expected)
        
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [b,c])
        result = shareMembers(g1, g2)
        
        # returned result is the number of id
        expected = set([2])
        self.assertTrue(result == expected)
        
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [b,a])
        result = shareMembers(g1, g2)
        
        # returned result is the number of id
        expected = set([2,1]) # It's OK if you reverse the order
        self.assertTrue(result == expected)
        
    def test_isPrime(self):
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [c,d])
        g3 = GroupContext(None, [e,f])
        
        result = isPrime(g1, [g2,g3])
        expected = True
        self.assertTrue(result == expected)
        
        g1 = GroupContext(None, [a,b])
        g2 = GroupContext(None, [c,d])
        g3 = GroupContext(None, [a,f])
        
        result = isPrime(g1, [g2,g3])
        expected = False # as g3 has 'a'
        self.assertTrue(result == expected)
        
    def test_remove(self):
        result = remove([a,b,c],c)
        expected = set([a,b])
        self.assertTrue(same(result,expected))
        
        result = remove([],c)
        expected = set([])
        self.assertTrue(same(result,expected))
        
        result = remove([a,b,c,d],a)
        #printList(result)
        expected = [a,b,d]
        #printList(expected)
        #print same(result, expected)
        self.assertFalse(same(result,expected))
        
    def test_removeList(self):
        result = remove([a,b,c],[b,c])
        expected = [a]
        self.assertTrue(same(result, expected))
        
        result = remove([a,b,c,d],[b,c])
        expected = [a,d]
        self.assertTrue(same(result, expected))
        
    def test_substract(self):
        #superSetGroupContext, subSetGroupContext):
        g = GroupContext(None, [a,b,c])
        
        result = substract(g, c)
        expected = GroupContext(None, [a,b])
    
        self.assertTrue(result == expected)
        
        # Check if the remaining group's member is one turn it into context
        g = GroupContext(None, [a,c])
        result = substract(g, c)
        expected = a
        self.assertTrue(expected == result)
        self.assertFalse(expected != result)
        
    def test_substract2(self):
        """Check to return NULL, when inputs are the same
        """
        #superSetGroupContext, subSetGroupContext):
        g1 = GroupContext(None, [a,b,c])
        g2 = GroupContext(None, [a,b,c])
        
        result = substract(g1, g2)
        self.assertTrue(result is None)
        
    def test_findSuperset1(self):
        ci = Context(1, 10)
        b = Context(2, 20)
        result = findSuperset(ci, b)
        assert result is None
        self.assertEqual(result, None)
        
    def test_findSuperset2(self):
        ci = Context(1, 10)
        
        g1 = GroupContext(15, [ci, b])
        result = findSuperset(ci, [g1])
        expected = set([g1])
        self.assertEqual(result, expected)
        
        # ci (id=1) doesn't belong to b/c
        g2 = GroupContext(20, [b,c])
        result = findSuperset(ci, [g1,g2])
        expected = set([g1])
        self.assertEqual(result, expected)
        
        # ci (id=1) doesn't belong to d/c
        g3 = GroupContext(20, [c,d])
        result = findSuperset(ci, [g3,g2])
        expected = set([])
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)