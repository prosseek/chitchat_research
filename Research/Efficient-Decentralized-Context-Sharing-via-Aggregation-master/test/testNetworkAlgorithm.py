import unittest
import sys

sys.path.append("../src")

from networkAlgorithm import *

class TestNetworkAlgorithm(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_node(self):
        n = NetworkAlgorithm.Node(10)
        n.add(20, 4)
        n.add(30, 5)
        
        self.assertTrue(n.neighbors[20], 4)
        self.assertTrue(n.neighbors[30], 5)
        
    def test_read(self):
        d = NetworkAlgorithm()
        # Exception error is expected
        self.assertRaises(Exception, d.read, "aha.txt")
        
        d.read("./testFile/dijkstraTest.txt")
        # 'A' (65) has neihbors 20,80,90
        self.assertTrue({66: 20, 68: 80, 71: 90} == d['A'].neighbors)
    
    def test_getNodes(self):
        d = NetworkAlgorithm()
        d.read("./testFile/dijkstraTest.txt")
        self.assertTrue(sorted(d.getNodes()) == sorted([65, 66, 67, 68, 69, 70, 71, 72]))
        
    def test_shortestPath(self):
        d = NetworkAlgorithm()
        d.read("./testFile/dijkstraTest.txt")
        res = d.shortestPathAll('A')
        self.assertTrue(
          [(65, 0, -1), (66, 20, 65), (70, 30, 66), (67, 40, 70), 
           (68, 50, 67), (72, 60, 67), (71, 70, 68), (69, 1000000, -1)] == sorted(res, key=lambda x: x[1]))
           
    def test_shortestPath2(self):
        d = NetworkAlgorithm()
        res = d.read("./testFile/network1.txt")
        res = d.shortestPathAll(1)
        expected = set([(3, 2, 2), (7, 4, 6), (4, 3, 3), (8, 5, 7), (2, 1, 1), (5, 4, 4), (1, 0, -1), (6, 3, 3)])
        self.assertTrue(sorted(res) == sorted(expected))
        
    def test_findShortestPathTrace(self):
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        paths = set([(3, 2, 2), (7, 4, 6), (4, 3, 3), (8, 5, 7), (2, 1, 1), (5, 4, 4), (1, 0, -1), (6, 3, 3)])
        res = d.findShortestPathTrace(paths, 1, 8)
        expected = [1, 2, 3, 6, 7, 8]
        self.assertTrue(res == expected)
        
    def test_findShortestPathTrace2(self):
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        paths = set([(3, 2, 2), (7, 4, 6), (4, 3, 3), (8, 5, 7), (2, 1, 1), (5, 4, 4), (1, 0, -1), (6, 3, 3)])
        res = d.findShortestPathTrace(paths, 2, 5)
        expected = [2, 3, 4, 5]
        self.assertTrue(res == expected)
        
    def test_findShortestPath(self):
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        res = d.shortestPath(2, 5)
        expected = (3, [2, 3, 4, 5])
        self.assertTrue(res, expected)
        
    def test_findShortestPath2(self):
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        res = d.shortestPath(5, 1)
        #print res
        expected = (3, [2, 3, 4, 5])
        self.assertTrue(res, expected)
        
    def test_findShortestPath3(self):
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        res = d.shortestPath(8, 5)
        #Aprint res
        expected = (3, [2, 3, 4, 5])
        self.assertTrue(res, expected)
        
    def test_findLongestShortestPath(self):
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        res = d.findLongestShortestPath()
        expected = [[1, 2, 3, 6, 7, 8], [5, 4, 3, 6, 7, 8], [8, 7, 6, 3, 4, 5], [8, 7, 6, 3, 2, 1]]
        self.assertTrue(sorted(res) == sorted(expected))
        
    def test_findMaxLengthNode(self):
        inp = set([(3, 2, 2), (7, 4, 6), (4, 3, 3), (8, 5, 7), (2, 1, 1), (5, 4, 4), (1, 0, -1), (6, 3, 3)])
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        result = d.findMaxLengthNode(inp)
        expected = 5
        self.assertTrue(expected == result)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)