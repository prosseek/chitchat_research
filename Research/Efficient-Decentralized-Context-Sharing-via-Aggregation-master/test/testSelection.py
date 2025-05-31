import unittest
import sys

sys.path.append("../src")

from context import *
from groupContext import *
from buffer import *
from selection import *

a = Context(1, 10)
b = Context(2, 20)
c = Context(3, 30)
d = Context(4, 40)
e = Context(5, 50)
f = Context(6, 60)
neighbors = ['h1']

class TestSelection(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_selectionForSingleCase3(self):
        """For debugging purpose
        It should not send the sender information to the sender
        """
        inputDictionary = {'h1':[c]}
        currentInputDictionary = {}
    
        outputBuffer = Buffer()
        outputBuffer.singleContexts = [a,b,c,d]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.singleContexts = [a,b] # only c,d will be sent
        sentHistoryDict = {'h1':[c]}
        sentHistory = SentHistory()
        sentHistory.addDictionary(sentHistoryDict)
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'sentHistory':sentHistory,
             'neighbors':neighbors}
             
        s = Selection(**i)
        dictionary = s.run(s = True)
        #printList(dictionary['h1'])
        #print dictionary['h1']
        self.assertTrue(same([d], dictionary['h1']))    
    
    def test_selectionForSingleCase1(self):
        inputDictionary = {'h1':[a]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.singleContexts = [a,b,c,d]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.singleContexts = []
        sentHistoryDict = {'h1':[c]}
        sentHistory = SentHistory()
        sentHistory.addDictionary(sentHistoryDict)
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'sentHistory':sentHistory,
             'neighbors':neighbors}
             
        s = Selection(**i)
        dictionary = s.run(s = True)
        #printList(dictionary['h1'])
        self.assertTrue(same([b,d], dictionary['h1']))
        
    def test_selectionForSingleCase2(self):
        neighbors = ['h1','h2']
        inputDictionary = {'h1':[a], 'h2':[b]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.singleContexts = [a,b,c,d]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.singleContexts = []
        sentHistoryDict = {'h1':[c], 'h2':[d]}
        sentHistory = SentHistory()
        sentHistory.addDictionary(sentHistoryDict)
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'sentHistory':sentHistory,
             'neighbors':neighbors}
             
        s = Selection(**i)
        dictionary = s.run(s = True)
        #printList(dictionary['h1'])
        self.assertTrue(same([b,d], dictionary['h1']))
        self.assertTrue(same([a,c], dictionary['h2']))
        
    def test_run1(self):
        # case 1:
        #  When outputBuffer is the same as previous one. There is nothing to send
        inputDictionary = {'h1':[a,b]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        oldOutputBuffer = Buffer()
        oldOutputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'neighbors':neighbors}
        s = Selection(**i)
        dictionary = s.run()
        #printList(dictionary['h1'])
        self.assertTrue(len(dictionary) == 0)
    
    def test_run2(self):
        # case 2:
        #  aggregated - (a,b,c,d)
        #  from h1 node [a,b]
        #  It just sends aggregated value to h1 only
        inputDictionary = {'h1':[a,b]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        oldOutputBuffer = Buffer()
        oldOutputBuffer.aggregatedContext = GroupContext(None, [a,b,c])
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'neighbors':neighbors}
        s = Selection(**i)
        dictionary = s.run()
        
        #printList(dictionary['h1'])
        self.assertTrue(len(dictionary['h1']) == 1)
        self.assertTrue(dictionary['h1'][0] == outputBuffer.aggregatedContext)
        
    def test_run3(self):
        # case 3:
        #  aggregated - (a,b,c,d)
        #  single - [e,f]
        #  from h1 node [a,b]
        #  
        # aggregated + e,f
        inputDictionary = {'h1':[a,b]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        outputBuffer.singleContexts = [e,f]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.aggregatedContext = GroupContext(None, [a,b,c])
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'neighbors':neighbors}
        s = Selection(**i)
        dictionary = s.run()
        
        expected = [outputBuffer.aggregatedContext, e, f]
        self.assertTrue(len(dictionary['h1']) == len(expected))
        self.assertTrue(same(dictionary['h1'], expected))
        
    def test_run4(self):
        # case 4:
        #  aggregated - (a,b,c,d)
        #  single - [e,f]
        #  from h1 node [e]
        # 
        #  send: aggregated + f
        inputDictionary = {'h1':[e]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        outputBuffer.singleContexts = [e,f]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.aggregatedContext = GroupContext(None, [a,b,c])
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'neighbors':neighbors}
        s = Selection(**i)
        dictionary = s.run()
        
        expected = [outputBuffer.aggregatedContext, f]
        self.assertTrue(len(dictionary['h1']) == len(expected))
        self.assertTrue(same(dictionary['h1'], expected))
        
    def test_run0(self):
        # case 5:
        #  aggregated - (a,b,c,d)
        #  prev - (a,b,c)
        #  from h1 node (d,e)
        # 
        #  send: None
        inputDictionary = {'h1': [GroupContext(None,[d,e])]}
        currentInputDictionary = {}

        outputBuffer = Buffer()
        outputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        #outputBuffer.singleContexts = [e,f]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.aggregatedContext = GroupContext(None, [a,b,c])
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'neighbors':neighbors}
        s = Selection(**i)
        dictionary = s.run()
        #print dictionary
        expected = []
        #printList(dictionary['h1'])
        #print dictionary
        self.assertTrue(len(dictionary['h1']) == len(expected))
        self.assertTrue(same(dictionary['h1'], expected))
        
    def test_run6(self):
        # case 6:
        #  aggregated - (a,b,c,d)
        #  prev - (a,b,c)
        # 
        #  from h1 node (d,e)
        #  from h1 current (a,b,c,d) <-- We already have this
        #  send: None
        inputDictionary = {'h1': [GroupContext(None,[e,f])]}
        currentInputDictionary = {'h1': [GroupContext(None,[a,b,c,d])]}

        outputBuffer = Buffer()
        outputBuffer.aggregatedContext = GroupContext(None, [a,b,c,d])
        #outputBuffer.singleContexts = [e,f]
        oldOutputBuffer = Buffer()
        oldOutputBuffer.aggregatedContext = GroupContext(None, [a,b,c])
        
        i = {'inputDictionary':inputDictionary,
             'currentInputDictionary':currentInputDictionary,
             'outputBuffer':outputBuffer,
             'oldOutputBuffer':oldOutputBuffer,
             'neighbors':neighbors}
        s = Selection(**i)
        dictionary = s.run()
        #print dictionary['h1'][0]
        #expected = [e,f]
        expected = []
        self.assertTrue(len(dictionary['h1']) == len(expected))
        self.assertTrue(same(dictionary['h1'], expected))
        #sys.exit(0)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
