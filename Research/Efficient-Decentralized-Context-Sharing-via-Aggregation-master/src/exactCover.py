import sys

class ExactCover(object):
    def __init__(self): 
        pass
        
    def solve(self, universe, C):
        #print X, Y
        universe = {j: set(filter(lambda i: j in C[i], C)) for j in universe}
        #print X
        return self._solve(universe, C)
        
    def _solve(self, X, Y, solution=[]):
        #print "*" * 10, "\nin solve"
        #print X, solution
        #print 
        #print universe
        if not X:
            # print "solution, not X", solution
            #print "***>>>"
            #print solution
            return list(solution)
        else:
            result = None
            c = min(X, key=lambda c: len(X[c]))
            #print "max as c list(X[c])", c, list(universe[c])
            for r in list(X[c]):
                # print "r", r
                # print "list[X[c]]", list(X[c])
                solution.append(r)
                cols = self.select(X, Y, r)
                #print cols
                #print X
                #print Y
                #print r
                result = self._solve(X, Y, solution)
                # print "res from solve:", result
                # #for s in solve(X, Y, solution):
                # #    return s
                #print X
                #print "reverted", r
                self.deselect(X, Y, r, cols)
                solution.pop()
                #print "solution", solution

            # There is a missing item, so return with None
            #print "RETURN from else", result, X
            return result

    def select(self, X, Y, r):
        #print "INX", X
        #print "INY", Y
        cols = []
        # r is 'A'
        # then j is 1,4,7
        for j in Y[r]:
            # print "j", j
            for i in X[j]:
                # then i is 'A','B'
                # print "i", i
                for k in Y[i]:
                    # i is 'A',
                    # k is '1,4,7'
                    if k != j: 
                        # print "remove i", i
                        # print "X[k]", X[k],k
                        X[k].remove(i)
                        # print "X[k]", X[k],k
                    #print "\n"
            # access X[j] and remove it
            cols.append(X.pop(j))
            #print X
            #print X[j]
        #print "COLS", cols, "R", r, "X", X, "Y", Y
        return cols

    def deselect(self, X, Y, r, cols):
        #print "unset"
        #print "FROM", X
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)
        #print "TO", X
 
    #print X

    #print filter(lambda i: 1 in Y[i], Y)

    #print X, Y
    # a = solve(X, Y)
    # print a
    
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testExactCover import *

    unittest.main(verbosity=2)