from contextShim import *
from struct import *
from util.util import *

class DatagramContextShim(ContextShim):
    def __init__(self): # , addr, port):
        super(DatagramContextShim, self).__init__()
        
    def getSendPacket(self, payLoad):
        contextBytes = self.getContextBytes()
        payloadLength = len(payLoad)
        bytesToSend = pack("i",payloadLength) + payLoad + contextBytes
        #dprint(bytesToSend)
        return bytesToSend
        
    def getReceivePacket(self, receivedData):
        # DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
        # while (receivePacket.getLength() < p.getLength() + PAYLOAD_LENGTH_FIELD_SIZE) {
        #     increaseReceiveBufferSize();
        #     receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
        # }
        # 
        # return receivePacket;
        return None # I don't think it's necessary for python implementation
        
    def processReceivedPacket(self, receivedData):
        #dprint(len(receivedData))
        # get the payload size
        payloadLength = unpack("i", receivedData[0:4])[0]
        #print payloadLength
        #print len("Hello, world")
        payload = receivedData[4:4+payloadLength]
        #print payload
        contextBytes = receivedData[4+payloadLength:]
        summaries = self.processContextBytes(contextBytes)
        #print summaries
        return payload, summaries
        
if __name__ == "__main__":
    import sys
    sys.path.append("../test")
    from testDatagramContextShim import *
    unittest.main(verbosity=2)