import sys
import os.path
sys.path.insert(0, "./src")

from network import *
from configuration import *

testSampleDirectory = getTestSimpleDirectory() # "/Users/smcho/temp/simulation"
dataDirectory = os.path.join(testSampleDirectory, "data")
outputDirectory = os.path.join(testSampleDirectory, "results")

def getFilePath(inputFile, resultDirectory, ext, name):
    fileName = os.path.split(inputFile)[1]
    fileWithoutExt = fileName.split('.')[0]
    return os.path.join(resultDirectory, fileWithoutExt + "_" + name + "." + ext)

def runSimulate(inputFile, singleOnly, resultDirectory = "./"):
    result = ""
    Network.s = singleOnly

    name = "S" if singleOnly else "A"
    
    n = Network(inputFile)
    
    dotFile = os.path.join(outputDirectory, "result.dot")
    n.dotGen(dotFile)

    Network.printStep = range(0,0)
    simulationSetup = {
        "endCount":100,
        "connectionBrokenRate":None,
        "missingDataRate":None}

    n.simulate(getSampleFile(), simulationSetup)
    a = n.analyzer

    print "Size: based on the steps"
    s1, s2 = a.getSize()
    print s1
    result += s1
    #print s2

    a0, a1, a2, cohorts = a.getAccuracy()
    string = "Accuracy: total"
    res = string + "\n" + printAccuracy(a0)
    print res
    
    result += res

    string = "Accuracy: agg"
    res = string + "\n" + printAccuracy(a1)
    print res
    result += res
    
    string = "Accuracy: single"
    #print a2
    res = string + "\n" + printAccuracy(a2)
    print res
    result += res

    string = "Accuracy: cohorts"
    res = string + "\n" + printAccuracyCohorts(cohorts)
    print res
    result += res
    
    f = getFilePath(inputFile, resultDirectory, "data" ,name)
    with open(f, "w") as a:
        a.write(result)

if __name__ == "__main__":    
    #singleOnly = True
    inputFile = "/Users/smcho/code/PycharmProjects/aggregator/data/test_data/square2.txt" # os.path.join(dataDirectory, "mesh" + str(i) + ".txt")
    print "PROCESSING: " + inputFile
    runSimulate(inputFile, True, outputDirectory)
    runSimulate(inputFile, False, outputDirectory)
    
    
    # for i in range(10, 20, 10):
    #     inputFile = os.path.join(dataDirectory, "mesh" + str(i) + ".txt")
    #     #f = os.path.join(inputFile, outputDirectory)
    #     print "PROCESSING: " + inputFile
    #     runSimulate(inputFile, True, outputDirectory)
    #     runSimulate(inputFile, False, outputDirectory)
    #     
    #     inputFile = os.path.join(dataDirectory, "tree" + str(i) + ".txt")
    #     #f = os.path.join(inputFile, outputDirectory)
    #     print "PROCESSING"  + inputFile
    #     runSimulate(inputFile, True, outputDirectory)  # single
    #     runSimulate(inputFile, False, outputDirectory)  # aggr
