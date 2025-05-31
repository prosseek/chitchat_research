"""
The simulation data
-------------------

The simulation data is stored in ``~/temp/simulation/data``, and they are generated
with `generateGraphs.py`.

The file format is ::

    [mesh|tree]NODESIZE_MAXWIDTH_MAXDEPTH_COUNT.txt

As long as NODESIZE is the same, they are in the same group of tests.

"""
import glob

import sys
import os.path
    
import datetime
import time

import gc

sys.path.insert(0, "./src")
from network import *
from tupleProcessor import TupleProcessor
from configuration import *

def getFilePath(inputFile, resultDirectory, ext, name):
    fileName = os.path.split(inputFile)[1]
    fileWithoutExt = fileName.split('.')[0]
    return os.path.join(resultDirectory, fileWithoutExt + "_" + name + "." + ext)

def runOneSimulate(inputFile, singleOnly):
    """
    It executes simulation on the inputFile (graph), and returns the result in
    one class object

    @singleOnly:
        When singleOnly is True, it runs without aggregation
    """

    result = {}
    sampleFile = "./test/testFile/sample.txt"
    Network.s = singleOnly
    #assert os.path.exists(inputFile)

    n = Network(inputFile)

    Network.printStep = range(0,0)
    n.simulate(sampleFile, endCount=100)
    a = n.analyzer

    result["packetCount"] = a.getFinalPacketNumber()
    # 'accuracy': (4.0, 4.0, 0.0, 0.0)
    # 1. 4.0 -> Total number of recognition
    # 2. 4.0 -> Total number of single context recognition
    # 3. 0.0 -> Total number of aggregated context count
    # 4. 0.0 -> Total number of cohorts
    # When you divide 3/4, you'll get the average number of elements in a cohort
    result["accuracy"] = a.getFinalAccuracy()
    result["speed"] = a.getFinalSpeed()

    gc.collect()
    return result

def get_average(input):
    a = TupleProcessor()
    s = 0.0
    c = TupleProcessor()
    for file in input:
        # get the average of packet number
        r = input[file]
        #print r
        a += r['accuracy']
        s += r['speed']
        c += r['packetCount']
    # get the average of accuracy
    size = len(input)
    return a/size, s/size, c/size

def runMassiveSimulation(pattern, singleOnly=True):
    files = glob.glob(pattern)
    #print pattern, files
    result = {}
    for f in files:
        print "Processing file - %s" % f
        result[f] = runOneSimulate(f, singleOnly)
        print result[f]

    if len(files) > 0:
        return get_average(result)
    else:
        #print >>sys.stderr, "No files in this pattern %s" % pattern
        raise Exception("No files in this pattern %s" % pattern)
        
def generatePrintResult(patternName, singleOnly, a,s,c):
    name = patternName + " " + str(singleOnly) + "\n"
    result = name + str(a) + "\n" + str(s) + "\n" + str(c) + "\n"
    return result

def printToFile(fileName, content):
    f = open(fileName, "a")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print >>f, st
    print >>f, content
    f.close()

if __name__ == "__main__":
    testPattern = "200_500_50_50"
    testSampleDirectory = os.path.join(getTestDirectory(), testPattern)
    print testSampleDirectory
    #sys.exit(0)
    # mesh
    #inputFile = os.path.join(testSampleDirectory,"mesh20_3_10_0.txt")
    #res = runOneSimulate(inputFile, singleOnly=False)
    #print res

    # pattern_name = "_mesh*.txt"
    # singleOnly = True
    # pattern = os.path.join(testSampleDirectory, pattern_name)
    # a,s,c = runMassiveSimulation(pattern, singleOnly=singleOnly)
    # p = generatePrintResult(pattern_name, singleOnly,a,s,c)
    # print p
    
    #all_patterns = (("mesh", "tree"), (True, False), range(10,101,10))
    resultFile = os.path.join(getResultsDirectory(), "result_%s.txt" % testPattern)

    all_patterns = (["mesh"], (False,), range(500,501,100))
    for types in all_patterns[0]:
        #print types, all_patterns[0]
        for singleOnly in all_patterns[1]:
            so = singleOnly
            for r in all_patterns[2]:
                pattern = types + str(r) + '_500*.txt'
                patternPath = os.path.join(testSampleDirectory, pattern)
                print pattern + " when singleOnly is " + str(so)
                try:
                    a,s,c = runMassiveSimulation(patternPath, singleOnly=singleOnly)
                    p = generatePrintResult(pattern, singleOnly,a,s,c)
                    printToFile(resultFile, p)

                except Exception as e:
                    print "             >> " + str(e)
