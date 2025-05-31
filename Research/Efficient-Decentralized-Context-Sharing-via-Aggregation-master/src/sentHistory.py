import sys
import os.path

from util import *

DEBUG = False

class SentHistory(object):
    def __init__(self):
        self.history = {}
        
    def __getitem__(self, number):
        if number in self.history:
            return self.history[number]
        else:
            return []
        
    def add(self, host, value):
        if host not in self.history:
            self.history[host] = set()
        
        if type(value) in [list, set]:
            for i in value:
                self.history[host].add(i)
        else:
            self.history[host].add(value)
        
    def addDictionary(self, dictionary):
        #print dictionary
        assert type(dictionary) is dict
        for i,v in dictionary.items():
            if type(v) in [set, list]:
                for e in v:
                    self.add(i, e)
            else:
                self.add(i, v)
        
    def sent(self, host, value):
        if host not in self.history:
            return False
            
        for i in self.history[host]:
            if i == value:
                return True
        
        return False
        
    def get(self, host):
        if host not in self.history:
            return {}
        else:
            return self.history[host]
        
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testSentHistory import *

    os.chdir("../test")
    unittest.main(verbosity=2)