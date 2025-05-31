import unittest
import sys

sys.path.append("../src")

from aggregationExceptions import *

class TestAggregationExceptions(unittest.TestCase):
    def setUp(self):
        pass
        
    @staticmethod
    def raise_NotGenerateGraphException(m):
        raise NotGenerateGraphException("Hello, error! > " + str(m))
        
    def test_NotGenerateGraphException(self):
        self.assertRaises(NotGenerateGraphException, TestAggregationExceptions.raise_NotGenerateGraphException, 10)
        try:
            TestAggregationExceptions.raise_NotGenerateGraphException(10)
        except Exception as e:
            self.assertTrue(str(e) == "Hello, error! > 10")

if __name__ == "__main__":
    unittest.main(verbosity=2)
    
#    if __name__ == "__main__":
#        import unittest
#        sys.path.append("../test")
#        from testExceptions import *
#        unittest.main(verbosity=2)