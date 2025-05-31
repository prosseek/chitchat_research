import random
import os
import sys

from treeGen import *
from aggregationExceptions import *

dotTemplate = """
graph graphname {
    %s
}
"""

class NetworkGen(object):
    def __init__(self):
        pass

    def makeSymmetric(self, dictionary):
        """
        Make the input dictionary as symmetric
        1:[2,3], 2:[0,3] --> 1:[2,3], 2:[0,1,3], 3:[1,2]
        """
        res = {}
            
        for i, elements in dictionary.items():
            if i not in res: res[i] = set()
            for e in elements:
                if e not in res: res[e] = set()
                res[e].add(i)
                res[i].add(e)
                
        for i, elements in res.items():
            #print elements
            res[i] = list(elements)
        
        #print res
        return res
        
    def getNodes(self, numberOfNode, exclude = None):
        if exclude is None: exclude = []
        assert numberOfNode < self.numberOfNodes
        values = set()
        i = len(values)
        while (i < numberOfNode):
            r = random.randint(0, self.numberOfNodes-1)
            if r not in exclude:
                values.add(r)
            i = len(values)
        return list(values)
        
    def getValue(self, maxValue = None):
        if maxValue is None: 
            maxValue = self.defaultMaxValue
        assert maxValue >= 0
        r = random.randint(0, maxValue)
        return r
        
    def generate_tree_network(self, node, depth = None, width = None, max_attempt = 300):
        if width is None:
            width = node / 3
        if depth is None:
            depth = node / 3
        tree_gen = TreeGen()
        tree, result_depth = tree_gen.generate(node, max_depth=depth, max_width=width, max_attempt=max_attempt)
        if result_depth > 0:
            tree = TreeGen.format_converter(tree)
            tree = self.makeSymmetric(tree)
            return tree
        else:
            raise NotGenerateGraphException("Tree not generated with params: node(%d),width(%d),depth(%d)" % (node, width, depth))

    def generate_mesh_file(self, file_path, tree, percentage = 0.3):
        mesh = TreeGen.tree_to_mesh(tree, percentage)
        NetworkGen.generate_tree_file_from_tree(file_path, mesh)
        return mesh

    def generate_tree_file(self, file_path, node, depth = None, width = None, max_attempt = 300):
        tree = self.generate_tree_network(node, depth=depth, width=width, max_attempt=max_attempt)
        NetworkGen.generate_tree_file_from_tree(file_path, tree)
        return tree

    @staticmethod
    def generate_tree_file_from_tree(file_path, tree):
        string = ""
        for key, value in sorted(tree.items()):
            string += "%d: " % key
            for i in value:
                string += "%d " % i
            string += "\n"
        
        with open(file_path, "w") as f:
            f.write(string)
            
    def dotGen(self, filePath, tree):
        string = ""
            
        cache = []
        for key, value in sorted(tree.items()):
            for i in value:
                if sorted((key,i)) not in cache:
                    string += "%d -- %d\n" % (key, i)
                    cache.append(sorted((key,i)))

        result = dotTemplate % string
        #print result
        if filePath:
            #print filePath
            with open(filePath, 'w') as f:
                f.write(result)
        return result
    
if __name__ == "__main__":
    os.chdir("../test")
    import unittest
    sys.path.append("../test")
    from testNetworkgen import *

    unittest.main(verbosity=2)