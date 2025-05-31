import unittest
import sys

sys.path.append("../src")

from exactCover import *
from util import *

class TestExactCover(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_cover(self):
        X = {1, 2, 3, 4, 5, 6, 7}
        Y = {
            'A': [1, 4, 7],
            'B': [1, 4],
            'C': [4, 5, 7],
            'D': [3, 5, 6],
            'E': [2, 3, 6, 7],
            'F': [2, 7]}
        ec = ExactCover()
        result = ec.solve(X,Y)
        expected = ['B','F','D']
        self.assertTrue(same(result, expected)) 
    
    def test_cover2(self):
        X = {1, 2, 3, 4}
        Y = {
            1: [1, 2],
            2: [2, 3],
            3: [3, 4],
            4: [4, 1]}
        ec = ExactCover()
        result = ec.solve(X,Y)
        expect1 = [1,3]
        expect2 = [2,4]
        self.assertTrue(same(result, expect1) or same(result, expect2))
        #expected = ['B','F','D']
        #self.assertTrue(same(result, expected)) 

if __name__ == "__main__":
    unittest.main(verbosity=2)