import sys
sys.path.insert(0, "./src")

from networkgen import *
import configuration
import glob

def printOK(filePath):
    print "%s file is created" % filePath
    
def printError(filePath):
    print >> sys.err, "%s file is created" % filePath

def generateOneGraph(node, depth, width, count, directory, density):
    tree_name = "tree" + str(node) + "_" + str(depth) + "_" + str(width) + "_" + str(count)
    mesh_name = "mesh" + str(node) + "_" + str(depth) + "_" + str(width) + "_" + str(density) + "_" + str(count)
    #print tree_name
    #print mesh_name
    dataDirectory = directory
    treeFilePath = os.path.join(dataDirectory, tree_name + ".txt")
    meshFilePath = os.path.join(dataDirectory, mesh_name + ".txt")
    treeDotFilePath = os.path.join(dataDirectory, tree_name + ".dot")
    meshDotFilePath = os.path.join(dataDirectory, mesh_name + ".dot")
    
    #print treeFilePath
    #print meshFilePath
    
    c = NetworkGen()
    try:
        tree = c.generate_tree_file(treeFilePath, node, depth=depth, width=width)
        #printOK(treeFilePath)
        c.dotGen(treeDotFilePath, tree)
        #printOK(treeDotFilePath)
        #print tree
    except NotGenerateGraphException as e:
        printError(treeFilePath)
        return False
        
    # Now, mesh file is generated
    try:
        mesh = c.generate_mesh_file(meshFilePath, tree, density)
        #printOK(meshFilePath)
        c.dotGen(meshDotFilePath, mesh)
        #printOK(meshDotFilePath)
    except NotGenerateGraphException as e:
        printError(meshFilePath)
        return False
        
    return True
    
def findMatchingMeshName(treeName):
    """
    tree30_30_2_0.txt matches
    mesh30_30_2_0.8_0.txt
    
    Given tree return the matching file in a directory
    """
    containingDirectory = os.path.split(treeName)[0]
    nameOnly = os.path.split(treeName)[1]
    
    treeComponent = nameOnly.replace("tree","mesh").split("_")
    #  < 0      < 1    < 2   < 3
    # ['mesh30', '15', '100', '80.txt']
    treeComponent.insert(3, "*")
    pattern = os.path.join(containingDirectory, "_".join(treeComponent))
    
    globResult = glob.glob(pattern)
    
    if len(globResult) == 0: 
        return None
    else: 
        return globResult[0]

def generateGraphs(totalSize, factor, node, depth, width, directory, density = 0.4):
    """
    It looks into the directory to count the number of files already generated.
    It **tries** to generate totalSize of circuits from them
   
    @totalSize: number of graphs generated 

    @node: total number of nodes
    @depth: maximum depth
    @width: maximum width
    @type: "tree" or "mesh" (default is tree)
    @density: when "mesh" graph, the generated number of edges. If it's 0.4, the generated number
              will be the number of exisiting edges * 0.4
    """
    
    ## Get the number of exisiting graphs
    expected_to_generate = int(totalSize/factor)
    pattern = "tree" + str(node) + "_*.txt"
    globintputTree = os.path.join(directory, pattern)
    resTree = glob.glob(globintputTree)
    
    pattern = "mesh" + str(node) + "_*.txt"
    globintputMesh = os.path.join(directory, pattern)
    resMesh = glob.glob(globintputMesh)
    
    if len(resTree) != len(resMesh):
        files = []
        print >> sys.stderr, "Tree and Mesh generation mismatch tree(%d) - mesh(%d)" % (len(resTree), len(resMesh))
        for i in resTree:
            matchingMesh = findMatchingMeshName(i)
            #print matchingMesh
            if matchingMesh is None:
                print >> sys.stderr, "No matching mesh for tree %s - reduce density" % i
                files.append(i)
        for i in files:
            print "removing file %s" % i
            os.unlink(i)
            dotFile = i.replace("txt","dot")
            os.unlink(dotFile)
        sys.exit(0)

    #smcho
    res = glob.glob(globintputTree)
    totalGeneratedSoFar = len(res)
    generatedFileCount = 0
    attemptCount = 0
    
    print generatedFileCount
    print totalSize
    print generatedFileCount < expected_to_generate and (generatedFileCount + totalGeneratedSoFar < totalSize)
    
    while generatedFileCount < expected_to_generate and (generatedFileCount + totalGeneratedSoFar < totalSize):
        result = generateOneGraph(node, depth, width, totalGeneratedSoFar + generatedFileCount, directory, density)
        attemptCount += 1
        
        if result:
            generatedFileCount += 1
        else:
            print >> sys.stderr, "Couldn't generated with %d/%d/%d" % (node, depth, width)
            raise Exception("Not generated file")
    
def minimumCheckedWidth(min, value):
    return value if value > min else min
                
def generateVaryingGraphs(totalSize, node, directory, density = 0.4):
    # very long graph
    generateGraphs(totalSize = totalSize, factor = 5, node = node, depth = node, width = minimumCheckedWidth(2, int(0.15*node)), directory=directory, density = density)
    generateGraphs(totalSize = totalSize, factor = 5, node = node, depth = node, width = minimumCheckedWidth(3, int(0.25*node)), directory = directory, density = density)
    generateGraphs(totalSize = totalSize, factor = 5, node = node, depth = node, width = minimumCheckedWidth(3, int(node*0.5)), directory= directory, density = density)
    generateGraphs(totalSize = totalSize, factor = 5, node = node, depth = node, width = minimumCheckedWidth(3, int(node*0.75)), directory = directory, density = density)
    # very wide graph
    generateGraphs(totalSize = totalSize, factor = 5, node = node, depth = node/2, width = totalSize, directory = directory, density = density)

if __name__ == "__main__":
    density = 0.1
    totalSize = 100
    
    nodeFrom = 10
    nodeTo = 100
    incre = 10
    
    # density = 0.8
    # totalSize = 100
    # 
    # nodeFrom = 10
    # nodeTo = 100
    # incre = 10
    
    directoryNameDensity = density
    resultDirName = "%d_%d_%d_%d" % (nodeFrom, nodeTo, incre, int(directoryNameDensity*100))
    directory = os.path.join(configuration.getTestDirectory(), resultDirName)
    print directory
    #sys.exit(0)
    if os.path.exists(directory):
        print "YES %s exists" % directory
    else:
        message = "%s does not exist: creating one" % directory
        print message
        os.mkdir(directory)
    for i in [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]:
        generateVaryingGraphs(totalSize = totalSize, node = i, directory = directory, density = density)