import copy
import time

class ContextSummary(object):
    def __init__(self, uid, db = None, hops = 3, timestamp = None):
        if timestamp is None: timestamp = time.time()
        if db is None: db = {}
        
        self.db = db
        self.uid = uid
        #self.tau = tau
        self.hops = hops
        self.timestamp = timestamp
        
    def __str__(self):
        return "(%d)[%d]:%s - (%s)" % (self.uid, self.hops, str(self.db), self.timestamp)
        
    def __eq__(self, other):
        #print type(self.timestamp)
        # http://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
        return self.sameExceptHops(other) and (self.hops == other.hops) 
               
    def sameExceptHops(self, other):
        return (self.uid == other.uid) and (self.db == other.db) \
               and  (abs(self.timestamp - other.timestamp) < 0.009)
               
    def size(self):
        return len(self.db)
    
    def keySet(self):
        return self.db.keys()
        
    def getTimestamp(self):
        return self.timestamp
    
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp
        
    def getId(self):
        return self.uid
        
    def setId(self, uid):
        self.uid = uid
        
    def get(self, key):
        if key in self.db:
            return self.db[key]
        return None
        
    def put(self, key, value):
        self.db[key] = value
        
    def containsKey(self, key):
        return key in self.db
        
    def remove(self, key):
        if self.containsKey(key):
            del self.db[key]
            
    def getWireCopy(self):
        # return new LabeledContextSummary(this);
        return copy.deepcopy(self)
        
    def getCopy(self):
        ### TEMP
        return self.getWireCopy()
        
    def incrementHops(self):
        #raise Exception("WHY???")
        self.hops += 1
        
    # def getTau(self):
    #     return self.tau;
    #     
    # def setTau(self, tau):
    #     self.tau = tau
        
    def getHops(self):
        return self.hops
        
    def setHops(self, hops):
        self.hops = hops
        
    # def getCopy(self):
    #     pass
        
if __name__ == "__main__":
    import sys
    sys.path.append("../test")
    from testContextSummary import *
    unittest.main(verbosity=2)
