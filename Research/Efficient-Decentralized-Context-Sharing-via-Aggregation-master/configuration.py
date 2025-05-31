import platform
import os.path

def get_testFile_directory():
    s = platform.system()

    if s == "Darwin":
        return "/Users/smcho/code/PycharmProjects/aggregator/test/testFile"
    elif s == "Linux":
        assert False, "Setup Linux configuration"

def return_darwin_linux(darwin, linux):
    s = platform.system()

    if s == "Darwin":
        assert os.path.exists(darwin), "Directory missing %s" % linux
        return darwin
    elif s == "Linux":
        assert os.path.exists(linux), "Directory missing %s" % linux
        return linux
    else:
        raise Exception("Only Mac or Linux is supported")
        

def getTestSimpleDirectory():
    darwin = "./test/testFile"
    linux = darwin
    return return_darwin_linux(darwin, linux)  
        
def getTestDirectory():
    darwin = "/Users/smcho/temp/simulation"
    linux = "/home/smcho/temp/simulation"
    return return_darwin_linux(darwin, linux)
    
def getResultsDirectory():
    return os.path.join(getTestDirectory(), "results")
    
def getDataDirectory():
    return os.path.join(getTestDirectory(), "data")
    
def getSampleFile():
    darwin = os.path.join(get_testFile_directory(), "sample.txt")
    darwin = os.path.abspath(darwin)
    return return_darwin_linux(darwin, darwin)
    
if __name__ == "__main__":
    print getTestSimpleDirectory()
    print getTestDirectory()
    print getSampleFile()
    print getResultsDirectory()
    print getDataDirectory()
    