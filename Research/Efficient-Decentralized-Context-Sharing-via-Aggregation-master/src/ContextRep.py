from struct import *
from zlib import *
#import binascii
import sys

class ContextRep(object):
    def __init__(self, value, aggregation):
        self.value = value
        self.aggregation = aggregation
        self.byteStreamRes = None
        self.location = [0 for i in range(500/8 + 1)]
        for i in aggregation:
            position = i / 8
            bitPosition = i % 8
            self.location[position] = self.location[position] | 1 << bitPosition
            
        #print self.location
        
    def aggregationToBytestream(self):
        # 'd' means 8 bytes packing
        self.byteStreamRes = pack('d', self.value)
        self.byteStreamRes += bytearray(self.location)
        #print len(compress(str(self.byteStreamRes)))
        #print binascii.hexlify(self.byteStreamRes)
        return self.byteStreamRes
        
    def byteStreamToAggregation(self):
        self.value = unpack('d', self.byteStreamRes[0:8])[0]
        result = []
        for i, val in enumerate(self.byteStreamRes[8:]):
            if val != 0:
                for count, j in enumerate(range(8)):
                    # 0000111 => '1' '1' '1' and 0 ...
                    if (val & (1 << j)) >> j:
                        result.append(count + 8*i)
        #print result
        return result
                        
if __name__ == "__main__":
   import unittest
   sys.path.append("../test")
   from testContextRep import *
   unittest.main(verbosity=2)