# import threading
# 
# def task1():
#     pass
# def task2():
#     pass
# def task3():
#     pass
# def task4():
#     pass
# def task5():
#     pass
# def task6():
#     pass
# 
# def dep1():
#     t1 = threading.Thread(target=task1)
#     t2 = threading.Thread(target=task2)
#     t3 = threading.Thread(target=task3)
# 
#     t1.start()
#     t2.start()
#     t3.start()
# 
#     t1.join()
#     t2.join()
#     t3.join()
# 
# def  dep2():
#     t4 = threading.Thread(target=task4)
#     t5 = threading.Thread(target=task5)
# 
#     t4.start()
#     t5.start()
# 
#     t4.join()
#     t5.join()
# 
# def dep3():
#     d1 = threading.Thread(target=dep1)
#     d2 = threading.Thread(target=dep2)
# 
#     d1.start()
#     d2.start()
# 
#     d1.join()
#     d2.join()
# 
# d3 = threading.Thread(target=dep3)
# d3.start()
# d3.join()
import glob

import sys
import os.path
    
import datetime
import time

import Queue
import threading

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
        result[f] = runOneSimulate(f, singleOnly)

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
    testPattern = "10_100_10_80"
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

    q = Queue.Queue()
    all_patterns = (["mesh", "tree"], (True, False), range(10,31,10))
    for types in all_patterns[0]:
        #print types, all_patterns[0]
        for singleOnly in all_patterns[1]:
            so = singleOnly
            for r in all_patterns[2]:
                pattern = types + str(r) + '_*.txt'
                patternPath = os.path.join(testSampleDirectory, pattern)
                print pattern + " when singleOnly is " + str(so)
                try:
                    t = threading.Thread(target=runMassiveSimulation, args=(patternPath, singleOnly))
                    t.daemon = True
                    print "Threading start with %s %s" % (patternPath, str(singleOnly))
                    t.start()
                    # a,s,c = runMassiveSimulation(patternPath, singleOnly=singleOnly)
                    # p = generatePrintResult(pattern, singleOnly,a,s,c)
                    # printToFile(resultFile, p)

                except Exception as e:
                    print "             >> " + str(e)
    s = q.get()
    print s