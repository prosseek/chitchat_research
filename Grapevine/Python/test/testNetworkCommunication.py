import unittest
import sys
from socket import *
import time
import threading

sys.path.append("../src")

from contextSummary import *
from contextHandler import *

# This address should be retrieved automatically
BROADCAST_ADDRESS = "192.168.65.255"
PORT = 4499

class PingerThreadUdp (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run (self):
        #print 'start thread'
        # UDP (SOCK_DGRAM). Use TCP (SOCK_STREAM)
        # http://stackoverflow.com/questions/8194286/python-socket-example-why-this-program-stuck-in-recvfrom-with-udp
        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        time.sleep(0.1)
        cs.sendto('This is a test', (BROADCAST_ADDRESS, PORT))

class TestNetworkCommunication(unittest.TestCase):
    def setUp(self):
        self.inetAddress = BROADCAST_ADDRESS # BROADCAST_ADDRESS;
        self.pingPort = PORT
    
    def test_udp_broadcast(self):
        a = PingerThreadUdp()
        a.start()

        # connectionless communication
        cs = socket(AF_INET, SOCK_DGRAM)
        try:
            cs.bind((self.inetAddress, self.pingPort))
        except:
            print 'failed to bind'
            cs.close()
            raise
            cs.blocking(0)

        #cs.bind(('192.168.65.255', port))
        data = cs.recvfrom(20)
        cs.close()
        self.assertTrue(data[0], 'This is a test')
        #  netcat -u 192.168.1.3 44444
        # http://stackoverflow.com/questions/10887844/python-and-udp-listening
        
    # def test_basic(self):
    #     # def __init__(self, uid, db, hops = 3, timestamp = None):
    #     # The id should be retreived from the 
    #     # UUID macUuid = UUID.nameUUIDFromBytes(macAddress);
    #     # id = macUuid.hashCode();
    #                     
    #     summary = ContextSummary(1);
    #     summary.put("test value 1", 1);
    #     summary.put("test value 2", 2);
    #     #print summary.db
    #     
    #     handler = ContextHandler.getInstance()
    #     handler.updateLocalSummary(summary)
    #     
    #     # byte[] message = "PING MESSAGE".getBytes();
    #     # DatagramPacket packet = new DatagramPacket(message, message.length, BROADCAST_ADDRESS,
    #     #                                            PING_PORT);
    # 
    #     # DatagramSocket socket = new ContextShimmedDatagramSocket();
    #     # socket.send(packet);

if __name__ == "__main__":
    unittest.main(verbosity=2)