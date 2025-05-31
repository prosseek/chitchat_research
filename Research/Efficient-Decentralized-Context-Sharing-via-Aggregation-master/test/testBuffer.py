import unittest
import sys

sys.path.append("../src")

from buffer import *

class TestBuffer(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)