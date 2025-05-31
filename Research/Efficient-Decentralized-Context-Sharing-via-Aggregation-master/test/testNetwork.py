import unittest
import sys
import os.path

#print os.path.abspath(".")
sys.path.append(os.path.abspath("../src"))
#print sys.path
from network import *
from networkAlgorithm import *
from configuration import *

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def test_drop_rate_is_one(self):
        n = Network("testFile/network1.txt")
        simulationSetup = {
            "endCount":100,
            "connectionBrokenRate":1.0,
            "missingDataRate":0.0}

        n.simulate(getSampleFile(), simulationSetup)
        
if __name__ == "__main__":
    import os
    unittest.main(verbosity=2)