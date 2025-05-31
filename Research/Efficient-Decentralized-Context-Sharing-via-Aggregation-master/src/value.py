import sys

class Value(object):
    def __init__(self, value, range = None):
        self.value = value
        if range is None:
            self.range = [value, value]
        else:
            self.range = range
            
    def __eq__(self, other):
        """Value equal operator
        
        This operation checks if the two values are the same
        """
        if self.range == other.range and self.value == other.value:
            return True
        return False
            
    def setValue(self, value):
        self.value = value
    def getValue(self):
        return self.value
    def setRange(self, range):
        self.range = range
    def getRange(self):
        return self.range
        
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testValue import *
    
    unittest.main(verbosity=2)