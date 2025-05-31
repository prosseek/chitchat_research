import unittest
import sys

sys.path.append("../src")

JYTHON = False
try:
    from graphDisplay import *
except ImportError:
    JYTHON = True
    pass

class TestGraphDisplay(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_A(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)