"""
graphStatistics:
given a pattern of files, it retursn the statistics over the files.

example:
    input: mesh10_
    
algorithm:
    1. gets all the files with pattern `mesh10_*`
    2. analyze
        the number of edges (min, max, average)
        the maximum depth of the graph 
        the maximum width of the graph
        
Usage of other tools:
    1. Get the maximum depth    
        d = NetworkAlgorithm()
        d.read("./testFile/network1.txt")
        res = d.findLongestShortestPath()
    2. Get the width and depth
        a = Network("testFile/network1.txt")
        result = a.getNodes()
        result = a.getEdges()
"""

import configuration
import os.path
import glob
import sys

sys.path.append("./src")
from network import *

def _stat(list):
    mini = min(list)
    maxi = max(list)
    avg = 1.0*sum(list)/len(list)
    return mini, maxi, avg

def stat(n, e, d, w1, w2):
    min,max,avg = _stat(n)
    result = "Node:  min (%d) max (%d) avg(%d)\n" % (min, max, avg)
    min,max,avg = _stat(e)
    result += "Edge:  min (%d) max (%d) avg(%d)\n" % (min, max, avg)
    min,max,avg = _stat(d)
    result += "Depth: min (%d) max (%d) avg(%d)\n" % (min, max, avg)
    min,max,avg = _stat(w1)
    result += "Min Width: min (%d) max (%d) avg(%d)\n" % (min, max, avg)
    min,max,avg = _stat(w2)
    result += "Max Width: min (%d) max (%d) avg(%d)\n" % (min, max, avg)
    return result

def analyze(pattern):
    """
    Given pattern it returns a string that analyzes the files in the pattern
    """
    directory = configuration.getTestDirectory()
    filePattern = os.path.join(os.path.join(directory, "data"), pattern + "*.txt")
    files = glob.glob(filePattern)

    n = []
    e = []
    d = []
    w1 = []
    w2 = []
    for f in files:
        net = Network(f)
        # print n.getNumberOfNodes()
        # print n.getNumberOfEdges()
        # print n.getDepth()
        # print n.getWidth()
        n.append(net.getNumberOfNodes())
        e.append(net.getNumberOfEdges())
        d.append(net.getDepth())
        w1.append(net.getMinWidth())
        w2.append(net.getMaxWidth())

    return ("total number = %d\n" % len(files)) + stat(n=n, e=e, d=d, w1=w1, w2=w2)

if __name__ == "__main__":
    retriveNumber = 100
    print ("Pattern: tree%d_\n" % retriveNumber) + analyze("tree%d_" % retriveNumber)
