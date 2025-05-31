# http://www.youtube.com/watch?v=8Ls1RqHCOPw
import sys
import os
import re

from util import *

# def error(message):
#     print >> sys.stderr, message
#     sys.exit(-1)
    
class NetworkAlgorithm(object):
    class Node(object):
        def __init__(self, id, alias = None):
            self.id = id
            self.alias = alias
            self.neighbors = {}
        def add(self, to, weight):
            self.neighbors[to] = weight
            
        def getNeighbors(self):
            return self.neighbors
    
    def __init__(self):
        self.nodes = {}
        self.numberOfNodes = 0
        self.shortestPaths = {}
        
    def __getitem__(self, index):
        if type(index) is str:
            index = ord(index)
        return self.nodes[index]
        
    def getNodes(self):
        return self.nodes.keys()
        
    def read(self, filePath):
        if not os.path.exists(filePath):
            raise Exception("NO FILE %s" % filePath)
        else:
            with open(filePath) as f:
                for i in f: # f.readlines():
                    if ':' in i:
                        first, rest = getFirstRest(i)
                        fromNode = first
                        for j in rest:
                            toNode = j
                            weight = 1
                            
                            if fromNode not in self.nodes:
                                self.nodes[fromNode] = NetworkAlgorithm.Node(fromNode)
                            if toNode not in self.nodes:
                                self.nodes[toNode] = NetworkAlgorithm.Node(toNode)
                        
                            self.nodes[fromNode].add(toNode, weight)
                    else:
                        r = re.compile("^([^\s]+)\s+([^\s]+)\s+([^\s]+)$")
                        res = r.search(i)
                        if res:
                            fromNode = res.group(1)
                            toNode = res.group(2)
                            if type(fromNode) is str:
                                alias = fromNode
                                fromNode = ord(fromNode[1:-1])
                            if type(toNode) is str:
                                alias2 = toNode
                                toNode = ord(toNode[1:-1])
                            assert type(fromNode) is int
                            assert type(toNode) is int
                        
                            weight = res.group(3)
                            weight = int(weight)
                        
                            if fromNode not in self.nodes:
                                self.nodes[fromNode] = NetworkAlgorithm.Node(fromNode, alias)
                            if toNode not in self.nodes:
                                self.nodes[toNode] = NetworkAlgorithm.Node(toNode, alias2)
                        
                            self.nodes[fromNode].add(toNode, weight)
            self.numberOfNodes = len(self.nodes)
    
    def shortestPathAll(self, fromNode):
        def getMin(Q):
            res = sorted(Q, key=lambda n: n[1]) # res = (i,0,-1) <-- returns the path length
            return res[0]
            
        def remove(Q, shortestNode):
            Q = Q - set([shortestNode])
            return Q
            
        def getPathLength(Q, node):
            res = filter(lambda n: n[0] == node, Q)
            if len(res) > 0:
                return res[0][1] # [(0, 11, -1)]
            else: # It means that the node is not in Q
                return -1
            
        def update(Q, id, path, prev):
            #print Q
            oldValue = filter(lambda n: n[0] == id, Q)
            newValue = (id, path, prev)
            Q  = Q - set(oldValue)
            Q |= set([newValue])
            return Q
            
        # http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        if type(fromNode) is str: fromNode = ord(fromNode)
        
        if fromNode in self.shortestPaths:
            return self.shortestPaths[fromNode]
        
        Q = set()
        S = set()
        infinity = 1000000
        
        for i in self.getNodes():
            if fromNode == i:
                res = (i,0,-1)
            else:
                res = (i, infinity,-1) 
            Q.add(res)

        while len(Q):
            shortestNode = getMin(Q)

            shortestNodeId = shortestNode[0] # (4, 0, -1) <- nodeId, pathLength, prevNode
            shortestLength = shortestNode[1]
            
            Q = remove(Q, shortestNode)
            S |= set([shortestNode])
            
            neighbors = self[shortestNodeId].getNeighbors()
            if len(neighbors):
                for n, weight in neighbors.items():
                    length = getPathLength(Q, n)
                    if length > 0: # n should not be visited before
                        if length > weight + shortestLength: # find shorter path
                            Q = update(Q, n, weight + shortestLength, shortestNodeId)
                            
        self.shortestPaths[fromNode] = S
        return S
        
    def findShortestPathTrace(self, paths, fromNode, toNode):
        def findElement(paths, node):
            elem = filter(lambda x: x[0] == node, paths)
            if len(elem): return elem[0]
            return None
            
        assert fromNode != toNode
        maxLength = len(paths)
        
        count = 0
        f = findElement(paths, toNode)
        trace = [f[0]]
        search = f[2] # (1, 0, -1)
        while count < maxLength:
            f = findElement(paths, search)
            trace.insert(0, f[0])
            search = f[2]
            
            if search == -1: # find start node
                return trace
            if search == fromNode:
                trace.insert(0, fromNode)
                return trace
                
            count += 1
            
        return None
        
    def shortestPath(self, fromNode, toNode):
        paths = self.shortestPathAll(fromNode)
        #print paths
        result = filter(lambda x: x[0] == toNode, paths)
        
        if len(result):
            res = self.findShortestPathTrace(paths, fromNode, toNode)
            return result[0][1], res # [(3, 2, 2), (7, 4, 6), (4, 3, 3), (8, 5, 7) ... <- [0] gives first elem, [1] returns length
        return None, None

    def findMaxLengthNode(self, paths):
        # start node is the node that has the previous node as -1
        startNode = filter(lambda x: x[2] == -1, paths)[0][1]
        sortedOne = sorted(paths, key=lambda x: -x[1])[0] # (8, 5, 7)
        return sortedOne[1] # second item is the length
        
    def findLongestShortestPath(self):
        # phase 1, find the maximum path
        maxLength = 0
        for n in self.nodes:
            p = self.shortestPathAll(n)
            length = self.findMaxLengthNode(p)
            if maxLength < length:
                maxLength = length
                
        # phase 2, we know the max length, so find the path with length 5
        #print maxLength
        result = []
        for n in self.nodes:
            p = self.shortestPathAll(n)
            res = self.findPathLength(p, maxLength)
            if res is not None:
                for r in res:
                    result.append(r)
        return result
            
    def findPathLength(self, paths, length):
        start = filter(lambda x: x[2] == -1, paths)
        end = filter(lambda x: x[1] == length, paths)
        #print "Ha"
        #print start, end
        
        if not end:
            return None
        
        assert len(start) == 1
        startNode = start[0][0] # [(1, 0, -1)]
        
        result = []
        for e in end:
            endNode = e[0]
            r = self.findShortestPathTrace(paths, startNode, endNode)
            result.append(r)
        #print result
        return result
        
if __name__ == "__main__":
    os.chdir("../test")
    import unittest
    sys.path.append("../test")
    from testNetworkAlgorithm import *

    unittest.main(verbosity=2)