from socket import *

from datagramContextShim import *

class ContextShimmedDatagramSocket(object):
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.shim = DatagramContextShim()
        
        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
    def getSendPacket(self, payload):
        return self.shim.getSendPacket(payload)
        
    def receive(self):
        cs = socket(AF_INET, SOCK_DGRAM)
        try:
            cs.bind((self.addr, self.port))
        except:
            print 'failed to bind'
            cs.close()
            raise
            cs.blocking(0)

        #cs.bind(('192.168.65.255', port))
        data = cs.recvfrom(1024) # get 1024 bytes first
        cs.close()
        #print data
        #print len(data[0])
        payload, summaries = self.shim.processReceivedPacket(data[0])
        #print payload
        #print summaries
        return (payload, summaries)
        #print res
        
    def send(self, payload):
        # get the sendpacket
        sendPacket = self.getSendPacket(payload)
        #print sendPacket
        self.cs.sendto(sendPacket, (self.addr, self.port))
    
if __name__ == "__main__":
    import sys
    sys.path.append("../test")
    from testContextShimmedDatagramSocket import *
    unittest.main(verbosity=2)