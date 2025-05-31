import unittest
import sys

sys.path.append("../src")

from contextsForOneSimulator import *

class TestContextsForOneSimulator(unittest.TestCase):
    def setUp(self):
        self.a = getContextsForOneSimulator()
        self.b = getContextsForOneSimulator()
        
    def test_Simple(self):
        self.assertEqual(id(self.a), id(self.b))

    def test_send(self):
        expected = "Hello"
        self.a.sendContexts("a", "b", expected)
        result = self.b.receiveContexts("a")
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main(verbosity=2)
    
# if __name__ == "__main__":
#    import unittest
#    sys.path.append("../test")
#    from testContextsForOneSimulator import *
#    unittest.main(verbosity=2)