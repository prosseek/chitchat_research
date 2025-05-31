import unittest
import sys

sys.path.append("../src")

from maxCover import *
from util import *

class TestMaxCover(unittest.TestCase):
    def setUp(self):
        self.X = {
            'A': [1, 2, 3],
            'B': [3, 4],
            'C': [4, 5, 6]
        }
        self.m = MaxCover()

    def test_pathLength(self):
        l = self.m.pathLength(['A','C'], self.X)
        self.assertTrue(l == 6)
        l = self.m.pathLength(['A','B'], self.X)
        self.assertTrue(l == 5)

    def test_createUniverse(self):
        result = self.m.createUniverse(self.X)
        self.assertTrue(same(set([1,2,3,4,5,6]), set(result)))

    def test_findKeyFromValue(self):
        result = self.m.findKeyFromValue(1, self.X)
        self.assertTrue(result == 'A')

    def test_findKeyFromValue2(self):
        result = self.m.findKeyFromValue(45, self.X)
        self.assertTrue(result is None)

    def test_findMaximum(self):
        X = {
            'A': [1, 2, 3],
            'B': [3, 4],
            'C': [4, 5, 6,7,8,9,10]
        }
        #universe = self.m.createUniverse(X)
        key, value = self.m.findMaximum(X)
        self.assertTrue(value == len(X['C']))
        self.assertTrue(key == 'C')

    def test_findMaximum2(self):
        X = {0: [0, 6, 12], 1: [4, 5, 7, 8], 2: [4, 5, 6, 13], 3: [3, 5, 12, 13], 4: [5, 6, 7, 8, 13]}
        #universe = self.m.createUniverse(X)
        key, value = self.m.findMaximum(X)
        self.assertTrue(value == len(X[4]))
        self.assertTrue(key == 4)

    def test_findFriendEnemy1(self):
        X = {
            'A': [1, 2, 3],
            'B': [3, 4],
            'C': [4, 5, 6]
        }
        m = MaxCover()
        friend, enemy = m.findFriendEnemy(X, 'A')
        self.assertTrue(same(friend, ['C']))
        self.assertTrue(same(enemy, ['B']))
        
        friend, enemy = m.findFriendEnemy(X, 'B')
        self.assertTrue(same(friend, []))
        self.assertTrue(same(enemy, ['A','C']))
        
        friend, enemy = m.findFriendEnemy(X, 'C')
        self.assertTrue(same(friend, ['A']))
        self.assertTrue(same(enemy, ['B']))
        
    def test_findFriendEnemy2(self):
        X = {
            'A': [1, 2],
            'B': [2, 3, 4],
            'C': [3,4,5,8],
            'D': [5,6,7],
            'E': [7,8]
        }
        m = MaxCover()
        friend, enemy = m.findFriendEnemy(X, 'A')
        self.assertTrue(same(friend, ['C','D','E']))
        self.assertTrue(same(enemy, ['B']))
        
        friend, enemy = m.findFriendEnemy(X, 'B')
        self.assertTrue(same(friend, ['D','E']))
        self.assertTrue(same(enemy, ['A','C']))
        
        friend, enemy = m.findFriendEnemy(X, 'C')
        self.assertTrue(same(friend, ['A']))
        self.assertTrue(same(enemy, ['B','D','E']))
        
        friend, enemy = m.findFriendEnemy(X, 'D')
        self.assertTrue(same(friend, ['A','B']))
        self.assertTrue(same(enemy, ['C','E']))
        
        friend, enemy = m.findFriendEnemy(X, 'E')
        self.assertTrue(same(friend, ['A','B']))
        self.assertTrue(same(enemy, ['C','D']))
        
    def test_createY1(self):
        X = {
            'A': [1, 2, 3],
            'B': [3, 4],
            'C': [4, 5, 6]
        }
        #create a dictionary from key to [length, select, exclusive]
        Y = {
            'A': [3, set('C'), set('B')],
            'B': [2, set(),  set(['A', 'C'])],
            'C': [3, set('A'), set('B')]
            }
            
        m = MaxCover()
        result = m.createY(X)
        self.assertTrue(sameDictionary(Y, result))
        
    def test_createY2(self):
        X = {
            'A': [1, 2],
            'B': [2, 3, 4],
            'C': [3,4,5,8],
            'D': [5,6,7],
            'E': [7,8]
        }
        #create a dictionary from key to [length, select, exclusive]
        Y = {
            'A': [3, set(['C','D','E']), set('B')],
            'B': [2, set(['D','E']),  set(['A', 'C'])],
            'C': [3, set('A'), set(['B','D','E'])],
            'D': [3, set(['A','B']), set(['C','E'])],
            'E': [3, set(['A','B']), set(['C','D'])],
            }
            
        m = MaxCover()
        result = m.createY(X)
        self.assertTrue(sameDictionary(Y, result))
        
    def atest_solve1(self):
        X = {
            'A': [1, 2, 3],
            'B': [3, 4],
            'C': [4, 5, 6]
        }
            
        ec = MaxCover()
        result = ec.solve(X)
        #print "r", result
        expected = ['A','C']
        self.assertTrue(same(result, expected))
        
    def test_solve2(self):
        X = {
            'A': [1, 2],
            'B': [2, 3, 4],
            'C': [3,4,5,8],
            'D': [5,6,7],
            'E': [7,8]
        }
            
        ec = MaxCover()
        result = ec.solve(X)
        #print "r", result
        expected1 = ['A','C']
        expected2 = ['B','D']
        #print result
        self.assertTrue(same(result, expected1) or same(result, expected2))
        
    def test_solve3(self):
        X = {0: [1, 2], 1: [2, 3, 4], 2: [8, 3, 4, 5], 3: [5, 6, 7], 4: [8, 7]}
        ec = MaxCover()
        result = ec.solve(X)
        #print result
        expected1 = [2,0]
        expected2 = [1,3]
        # print expected
        # print result
        self.assertTrue(same(result, expected1) or same(result,expected2))
    #     
    def test_solve4(self): # for debugging in random15
        X = {0: [0, 6, 12], 1: [4,5,7,8], 2: [4,5,6,13], 3: [3,5,12,13], 4: [5,6,7,8,13]}
        ec = MaxCover()
        result = ec.solve(X)
        #print result
        expected = [0,1]
        self.assertTrue(same(result, expected))   
        
    def test_solve5(self): # for debugging in random15
        X = {0: [0,1], 1:[2,3], 2:[2,4], 3:[1,2,3,4]}
        ec = MaxCover()
        result = ec.solve(X)
        #print result
        expected1 = [0,1]
        expected2 = [0,2]
        expected3 = [3]
        #print result
        #print result
        # print result
        # print expected3
        # print same(result, expected3)
        self.assertTrue(same(result, expected1) or same(result,expected2) or same(result, expected3))   
    
    def test_cover(self):
        X = {1, 2, 3, 4, 5, 6, 7}
        Y = {
            'A': [1, 4, 7],
            'B': [1, 4],
            'C': [4, 5, 7],
            'D': [3, 5, 6],
            'E': [2, 3, 6, 7],
            'F': [2, 7]}
        ec = MaxCover()
        result = ec.solve(Y)
        expected = ['B','F','D']
        self.assertTrue(same(result, expected))
        
    def test_cover2(self):
        X = {1, 2, 3, 4}
        Y = {
            1: [1, 2],
            2: [2, 3],
            3: [3, 4],
            4: [4, 1]}
        ec = MaxCover()
        result = ec.solve(Y)
        expect1 = [1,3]
        expect2 = [2,4]
        self.assertTrue(same(result, expect1) or same(result, expect2))
    
        
if __name__ == "__main__":
    unittest.main(verbosity=2)