import unittest
import sys
import time
import threading
sys.path.append("../src")

from contextShimmedDatagramSocket import *
from contextSummary import *
from util.util import *
from contextHandler import *

BROADCAST_ADDRESS = "192.168.65.255"
PORT = 4499

class PingerThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run (self):
        # cs = socket(AF_INET, SOCK_DGRAM)
        # cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # 
        # time.sleep(0.1)
        # cs.sendto('This is a test', (BROADCAST_ADDRESS, PORT))
        summary = ContextSummary(1)
        summary.put("test value 1", 1)
        summary.put("test value 2", 2)

        handler = ContextHandler.getInstance();
        handler.updateLocalSummary(summary)
        socket = ContextShimmedDatagramSocket(BROADCAST_ADDRESS, PORT)
        time.sleep(0.1)
        socket.send("Hello world")

class TestContextShimmedDatagramSocket(unittest.TestCase):
    def setUp(self):
        self.c = ContextShimmedDatagramSocket(BROADCAST_ADDRESS, PORT)
        
    def test_broadcast(self):
        a = PingerThread()
        a.start()
        
        payload, summaries = self.c.receive()
        self.assertTrue(2, summaries[0].get("test value 2"))
        self.assertTrue(1, summaries[0].get("test value 1"))
        
        handler = ContextHandler.getInstance()
        summary = handler.get(1)
        self.assertTrue(2, summary.get("test value 2"))
        self.assertTrue(1, summary.get("test value 1"))
        
if __name__ == "__main__":
    unittest.main(verbosity=2)