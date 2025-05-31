import networkx as nx
import matplotlib.pyplot as plt
import re

try:
    from networkx import graphviz_layout
except ImportError:
    raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")

class GraphDisplay(object):
    def __init__(self, networkFile):
        self.networkTopology = {}
        self.networkFile = networkFile
        self.networkFileParsing()
    
    def getFirstRest(self, l):
        """Separate first item and the rest 
    
        input: "1: 1 2 3 4 5"
        ouptut: 1, [1,2,3,4,5]
        """
        assert type(l) is str
    
        regex = re.compile("^(\d+):\s+((\d+\s*)+)")
        res = regex.search(l.rstrip())
        first = int(res.group(1))
        rest = map(lambda x: int(x), res.group(2).split(' ')) 
        return first, rest
    
    def networkFileParsing(self):
        if self.networkTopology: return self.networkTopology
        
        with open(self.networkFile, 'r') as f:
            for l in f:
                #print l.rstrip()
                first, rest = self.getFirstRest(l)
                self.networkTopology[first] = rest
        #print self.networkTopology

        return self.networkTopology
    
    def getEdges(self, topology):
        # input {1: [2, 3], 2: [1, 4], 3: [1, 4, 5], 4: [2, 3, 6], 5: [3, 6], 6: [4, 5, 7], 7: [6]}
        # output [(1,2),(1,3), ...]
        #print topology
        s = set()
        for key, value in topology.items():
            for i in value:
                s.add((key,i))
        #print list(s)
        return list(s)
        
    def getNodes(self, topology):
        # input {1: [2, 3], 2: [1, 4], 3: [1, 4, 5], 4: [2, 3, 6], 5: [3, 6], 6: [4, 5, 7], 7: [6]}
        # output [1,2,3,4,5,6,7]
        return topology.keys()
    
    def show(self):
        edges = self.getEdges(self.networkTopology)
        nodes = self.getNodes(self.networkTopology)
        
        G=nx.Graph()

        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        #print G.nodes()
        #print G.edges()

        pos=nx.graphviz_layout(G,prog='twopi',args='')
        #plt.figure(figsize=(8,8))
        # >>> nx.draw(G)
        # >>> nx.draw_random(G)
        # >>> nx.draw_circular(G)
        # >>> nx.draw_spectral(G)
        nx.draw_spectral(G) #,pos,node_size=300,alpha=0.5,node_color="blue", with_labels=True)
        #plt.axis('equal')
        #plt.savefig('circular_tree.png')
        plt.show()
        
if __name__ == "__main__":
    filePath = "../test/testFile/network2.txt"
    g = GraphDisplay(filePath)
    g.show()
