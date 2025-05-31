import sys

class NotGenerateGraphException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        
if __name__ == "__main__":
   import unittest
   sys.path.append("../test")
   from testAggregationExceptions import *
   unittest.main(verbosity=2)
    