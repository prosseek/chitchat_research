import inspect
import os.path
import sys

def removeAll(lists, removeLists):
    """
    Remove all of the removeLists from lists
    """
    result = []
    for member in lists:
        if member not in removeLists:
            result.append(member)
            
    return result
    
def dprint(string):
    # http://stackoverflow.com/questions/3711184/how-to-use-inspect-to-get-the-callers-info-from-callee-in-python
    # http://stackoverflow.com/questions/3056048/filename-and-line-number-of-python-script
    frame,filename,line_number,function_name,lines,index=\
            inspect.getouterframes(inspect.currentframe())[1]
    print >> sys.stderr,  str(string) + "\t\t\t(%s:%d)" % (os.path.basename(filename), line_number)