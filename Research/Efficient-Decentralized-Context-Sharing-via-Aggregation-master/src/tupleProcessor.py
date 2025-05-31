"""
Tuple processor processes tuples

ex) t = (1,2,3)
    t += (2,3,4) -> (3,5,7)

    t /= 2 -> (0.5, 1, 1.5)

Warning:
 1. only += and /= is supported
"""

class TupleProcessor(object):
    def __init__(self, tuple=None):
        if tuple is not None:
            self.tuple = list(tuple)
        else:
            self.tuple = []
        
    def __iadd__(self, other):
        if len(self.tuple) > 0:
            for i, val in enumerate(other):
                self.tuple[i] += val
        else:
            for i, val in enumerate(other):
                self.tuple.append(val)

        return self

    def __div__(self, value):
        if value != 0:
            result = map(lambda x: 1.0*x/value, self.tuple)
        return TupleProcessor(tuple(result))

    def getTuple(self):
        return tuple(self.tuple)

    def getList(self):
        return self.tuple
            
    def __str__(self):
        string = ""
        for i in self.tuple:
            string += str(i) + ","
        return string[0:len(string)-1]
        
    def __idiv__(self, value):
        if value != 0:
            self.tuple = map(lambda x: 1.0*x/value, self.tuple)
        return self

if __name__ == "__main__":
    import unittest
    import sys
    sys.path.append("./test")
    from testTupleProcessor import *

    unittest.main(verbosity=2)