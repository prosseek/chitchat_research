import unittest
import sys
import time
sys.path.append("../src")

from serializer import *

class TestSerializer(unittest.TestCase):
    def setUp(self):
        self.s = Serializer()
        
    def test_to_str(self):
        self.s.writeObjectData(123456, "int")
        # 1*256*256 + 226*256 + 64 == 123456
        #print self.s.__str__()
        #expected = "[64][226][1][0]"
        expected = "[0x40][0xe2][0x1][0x0]"
        #print self.s
        self.assertTrue(expected == self.s.__str__())
        
    def test_packInteger(self):
        res = self.s.writeObjectData(4, "int")
        expected = "[0x4][0x0][0x0][0x0]"
        #print self.s
        self.assertTrue(expected == self.s.__str__())
        
    def test_packString(self):
        res = self.s.writeObjectData("hello", "string")
        expected = "[0x68][0x65][0x6c][0x6c][0x6f]" # h e ll o
        # print self.s
        self.assertTrue(expected == self.s.__str__())
        
    def test_packIntegerAndString(self):
        res = self.s.writeObjectData(4, "int")
        res = self.s.writeObjectData("hello", "string")
        #print self.s
        expected = "[0x4][0x0][0x0][0x0][0x68][0x65][0x6c][0x6c][0x6f]"
        self.assertTrue(expected == self.s.__str__())
        
    def test_reset(self):
        res = self.s.writeObjectData(4, "int")
        self.assertTrue(len(res) == 4)
        self.s.reset()
        self.assertTrue(self.s.getResult() == "")
        
    def test_readObjectData(self): # , buffer, type):
        # def readObjectData(self, buffer, type):
        self.s.writeObjectData(4, "int")
        self.s.writeObjectData("hello", "string")
        
        #print self.s.to_string(self.s)
        result = self.s.readObjectData(self.s.result[0:4], "int")
        self.assertTrue(result, 4)
        
        result = self.s.readObjectData(self.s.result[4:4+5], "string")
        self.assertTrue(result, "hello")
        
    def test_autoReadObjectData(self):
        # def readObjectData(self, buffer, type):
        self.s.writeObjectData(4, "int")
        self.s.writeObjectData("hello", "string")
        timestamp = time.time()
        self.s.writeObjectData(timestamp, "timestamp")
        
        #print self.s.to_string(self.s)
        result = self.s.autoReadObjectData("int") # self.s.result[0:4], "int")
        self.assertTrue(result, 4)
        
        result = self.s.autoReadObjectData("string5") # self.s.result[4:4+5], "string")
        #print result
        self.assertTrue(result, "hello")
        
        result = self.s.autoReadObjectData("timestamp") # self.s.result[4:4+5], "string")
        
        # print float(result), type(float(result))
        # print timestamp, type(timestamp)
        # print abs(float(result) - timestamp)
        self.assertTrue(abs(float(result) - timestamp) < 0.00999)
        
    def test_readTimestamp(self):
        timestamp = time.time()
        #print timestamp
        self.s.writeObjectData(timestamp, "timestamp")
        timestampSerialized = self.s.result
        recoveredTimestamp = self.s.readObjectData(timestampSerialized, "timestamp")
        
        self.assertTrue(abs(float(recoveredTimestamp) - timestamp) < 0.00999)
        
    def test_size(self):
        self.s.writeObjectData(4, "int")
        self.assertTrue(self.s.size(), 4)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)