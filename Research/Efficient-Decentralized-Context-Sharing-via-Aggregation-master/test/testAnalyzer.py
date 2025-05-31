import unittest
import sys

sys.path.append("../src")

from analyzer import *
from network import *
    
def findCorrectTestFile(filePath):
    if not os.path.exists(filePath):
        filePath = os.path.join("../test", filePath)
        if not os.path.exists(filePath):
            print "ERROR!!!!!! %s" % os.path.abspath(filePath)
    return filePath

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.a = Analyzer(None)
        Network.s = True # Test for single case
        
        filePath = "./testFile/network1.txt"
        filePath = findCorrectTestFile(filePath)
            
        self.n = Network(filePath)
        # do not print any results
        Network.printStep = range(0,0)
        
        simulationFilePath = "./testFile/sample.txt"
        self.simulationFilePath = findCorrectTestFile(simulationFilePath)
        
    def test_getNodes(self):
        nodes = self.n.analyzer.getNodes()
        # The node size of network1 is 8
        #self.assertTrue(len(nodes) == 8)
        self.assertTrue(same(nodes, [1,2,3,4,5,6,7,8]))
    
    def test_getProgress(self):
        """
        TODO - broken test here
        """
        simulationSetup = {
            "endCount":100}
        self.n.simulate(self.simulationFilePath, simulationSetup)
        a = self.n.analyzer
        res = a.getProgress(1)
        #print res
        expect1 = """DB:Single:[(1)(2)]
DB:Single:[(1)(2)(3)]
DB:Single:[(1)(2)(3)(4)(6)]
DB:Single:[(1)(2)(3)(4)(5)(6)(7)]
DB:Single:[(1)(2)(3)(4)(5)(6)(7)(8)]
"""
        expect2 = """DB:Single:[(1)(2)(3)(4)(5)(6)(7)(8)]
DB:Single:[(1)(2)(3)(4)(6)]
DB:Single:[(1)(2)(3)]
DB:Single:[(1)(2)]
DB:Single:[(1)(2)(3)(4)(5)(6)(7)]
"""
        # expect2 is return from Jython
        self.assertTrue(res == expect1 or res == expect2)
        # print len(res)
        # print len(expect)
        
    def test_addDb(self):
        self.a.addDb(1, 2, 12)
        #self.a.getDb(1, 2)
        self.assertTrue(12 == self.a.getDb(1,2))
        self.a.addDb(2, 3, 11)
        self.assertTrue(11 == self.a.getDb(2,3))

    def test_getCommunicationCount(self):
        a = self.a
        a.add(0,1,2,None)
        result = a.getCommuncationCount()
        self.assertEqual(result, 1)
        
        a.add(0,1,3,None)
        result = a.getCommuncationCount()
        self.assertEqual(result, 2)
        
        a.add(1,1,2,None)
        result = a.getCommuncationCount()
        self.assertEqual(result, 3)
        
    def test_showSize(self):
        simulationSetup = {
            "endCount":100,
            "connectionBrokenRate":None,
            "missingDataRate":None}
        self.n.simulate(self.simulationFilePath, simulationSetup)

        a = self.n.analyzer
        res, size = a.getSize()
        self.assertTrue(size == 56)
        #print "???"
        
    def test_showAccuracy(self):
        Network.s = True
        simulationSetup = {
            "endCount":100}
        self.n.simulate(self.simulationFilePath, simulationSetup)
        a = self.n.analyzer
        ressTotal, res, resSingle, resCohorts = a.getAccuracy()
        self.assertTrue(len(res) == 5)
        self.assertTrue(res == resSingle)
        self.assertTrue(resSingle[5] == {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8})
        # print "--- RESTOTAL"
        # print ressTotal
        # print "--- RES"
        # print res
        # print "--- RES SINGLE"
        # print resSingle
        # print "--- RES COHORTS"
        # print resCohorts
        # print "***"
        
    def test_showAccuracy2(self):
        Network.s = False

        simulationSetup = {
            "endCount":100}
        self.n.simulate(self.simulationFilePath, simulationSetup)
        a = self.n.analyzer
        resTotal, res, resSingle, resCohorts = a.getAccuracy()
        #print resCohorts
        #print resTotal
        #print resSingle
        self.assertTrue(resTotal == {1: {1: 2, 2: 3, 3: 4, 4: 3, 5: 2, 6: 3, 7: 3, 8: 2}, 
            2: {1: 3, 2: 5, 3: 7, 4: 5, 5: 3, 6: 6, 7: 4, 8: 3}, 
            3: {1: 5, 2: 7, 3: 8, 4: 7, 5: 5, 6: 8, 7: 6, 8: 4}, 
            4: {1: 7, 2: 8, 3: 8, 4: 8, 5: 7, 6: 8, 7: 8, 8: 6}, 
            5: {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8}})
        self.assertTrue(len(res) == 5)
        self.assertTrue(res[5] == {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8})
        self.assertTrue(res != resSingle)
        self.assertTrue(resSingle[5] == {1: 4, 2: 4, 3: 8, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4})
        # At time step 5, node 1 has 2 cohorts, that comprises 4 elements. 
        self.assertTrue(resCohorts[5] == {1: [2, 4], 2: [2, 4], 3: [0, 0], 4: [2, 4], 5: [2, 4], 6: [2, 4], 7: [2, 4], 8: [2, 4]})
        
        # Compare the Single case
        Network.s = True # Test for single case
        filePath = "./testFile/network1.txt"
        filePath = findCorrectTestFile(filePath)
        n = Network(filePath)
        simulationFilePath = "./testFile/sample.txt"
        simulationFilePath = findCorrectTestFile(simulationFilePath)

        simulationSetup = {
            "endCount":100}
        n.simulate(self.simulationFilePath, simulationSetup)
        a = self.n.analyzer
        ressTotal, res2, resSingle2, resCohorts2 = a.getAccuracy()
        self.assertTrue(res == res2)
        
    def atest_getAccuracyHistoryForNode_test_for_network1_when_aggregate(self):
        filePath = "./testFile/network1.txt"
        self.test_getAccuracyHistoryForNode_test(filePath, True)
        
    ###
    # network, single/aggregated, expected values 
    def getAccuracyHistoryForNode_for_node1(self, filePath, single, exp1, exp2, node = -1):
        filePath = filePath
        single = single
        filePath = findCorrectTestFile(filePath)
        n = Network(filePath)
        Network.s = single

        simulationSetup = {
            "endCount":100,
            "connectionBrokenRate":None,
            "missingDataRate":None}
        n.simulate(self.simulationFilePath, simulationSetup)
        a = n.analyzer
        resultTotal, result, resultSingle, resultCohorts = a.getAccuracy()
        
        #print resultTotal
        
        res1 = a.getAccuracyHistoryForNode(result, node)
        #print >> sys.stderr, res1
        self.assertTrue(same(exp1, res1))
        res2 = a.getAccuracyHistoryForNode(resultSingle, node)
        #print >> sys.stderr, res2
        self.assertTrue(same(exp2, res2))
        
    def test_getAccuracyHistoryForNode_for_node1_singlecase(self):
        filePath = "./testFile/network1.txt"
        single = True
        exp1 = [0.25, 0.375, 0.625, 0.875, 1.0]
        exp2 = exp1
        self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2, 1)
        
    def test_getAccuracyHistoryForNode_for_node1_aggregatecase(self):
        filePath = "./testFile/network1.txt"
        single = False
        exp1 = [0.25, 0.375, 0.625, 0.875, 1.0] # sg + prime 
        exp2 = [0.25, 0.375, 0.375, 0.375, 0.5] # sg
        self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2, 1)
        
    def test_getAccuracyHistoryForNode_for_average_aggregatecase(self):
        filePath = "./testFile/network1.txt"
        single = False
        exp1 = [0.25, 0.5, 0.75, 0.875, 1.0] # sg + prime 
        exp2 = [0.25, 0.375, 0.375, 0.375, 0.5] # sg
        self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2)
        
    def test_getAccuracyHistoryForNode_for_average_singlecase(self):
        filePath = "./testFile/network1.txt"
        single = True
        exp1 = [0.25, 0.5, 0.75, 0.875, 1.0]
        #exp1 = [0.25, 0.375, 0.625, 0.875, 1.0] # sg + prime 
        exp2 = exp1 # sg
        self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2)
        
    ###############
    # network3
    def test_getAccuracyHistoryForNode_for_network3_node3_singlecase(self):
        filePath = "./testFile/network3.txt"
        single = True
        exp1 = [0.5714285714285714, 0.8571428571428571, 1.0, 1.0]
        exp2 = exp1
        self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2, 3)
        
    # def test0_getAccuracyHistoryForNode_for_network3_node3_aggregatecase(self):
    #     filePath = "./testFile/network3.txt"
    #     single = False
    #     exp1 = [0.5714285714285714, 0.8571428571428571, 1.0, 1.0] # sg + prime 
    #     exp2 = exp1 # [0.42857142857142855, 0.7142857142857143, 0.8571428571428571, 1.0] # sg
    #     self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2, 3)
        
    # def test_getAccuracyHistoryForNode_network3_average_aggregatecase(self):
    #     filePath = "./testFile/network3.txt"
    #     single = False
    #     exp1 = [0.42857142857142855, 0.7142857142857143, 0.8571428571428571, 1.0] # sg + prime 
    #     exp2 = [0.42857142857142855, 0.5714285714285714, 0.7142857142857143, 0.7142857142857143] # sg
    #     self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2)
        
    def test_getAccuracyHistoryForNode_network3_average_singlecase(self):
        filePath = "./testFile/network3.txt"
        single = True
        exp1 = [0.42857142857142855, 0.7142857142857143, 0.8571428571428571, 1.0]
        #exp1 = [0.25, 0.375, 0.625, 0.875, 1.0] # sg + prime 
        exp2 = exp1 # sg
        self.getAccuracyHistoryForNode_for_node1(filePath, single, exp1, exp2)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)