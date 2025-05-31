import sys
from copy import *
#count = 0

class MaxCover(object):
    def __init__(self): 
        self.solutionResults = []

    def createUniverse(self, X):
        universe = set()
        for value in X.values():
            universe |= set(value)
        return list(universe)

    def findKeyFromValue(self, val, map):
        for key, value in map.items():
            if val in value:
                return key
        return None

    def findMaximum(self, X):
        # X = {
        #     'A': [1, 2, 3],
        #     'B': [3, 4],
        #     'C': [4, 5, 6]
        # }
        # Universe = [1,2,3,4,5,6]
        #
        # cache[A] = 3 # A has three elements

        maxkey = None
        max = -1
        cache = {}

        for key, val in X.items():
            cache[key] = len(val)
            if max < len(val):
                max = len(val)
                maxkey = key
        return maxkey, max

        #for val in universe:
        #    key = self.findKeyFromValue(val, X)
        #    if key is not None:
        #        if max < cache[key]:
        #            maxkey = key
        #            max = cache[key]
        #return maxkey, max

    def findFriendEnemy(self, X, i):
        #print X
        temp = X[i]
        del X[i]
        
        #print X
        tempSet = set(temp)
        friendSet = set()
        enemySet = set()
        
        for j in X:
            jset = set(X[j])
            if tempSet & jset == set([]):
                # if there is an intersection, it's an enemy
                friendSet.add(j)
            else:
                enemySet.add(j)
            
        X[i] = temp
        #print friendSet
        #print enemySet
        return list(friendSet), list(enemySet)

    def pathLength(self, path, X):
        length = 0
        for p in path:
            length += len(X[p])
        return length

    def solve(self, X):
        Xp = deepcopy(X)
        path = []
        results = []
        self._solve(Xp.keys(), Xp, path, results)
        #print results
        max = -1
        maxPath = None
        for path in results:
            pathLength = self.pathLength(path, X)
            if pathLength > max:
                max = pathLength
                maxPath = path

        return maxPath

    def _solve(self, keys, X, cover, covers):
        if len(keys) == 0:
            p = deepcopy(cover)
            covers.append(p)
            return
        for key in keys:
            #print key, len(X[key])
            friendSet, enemySet = self.findFriendEnemy(X, key)
            #print "Friend:"
            #print friendSet
            Xp = deepcopy(X)
            del Xp[key]
            for e in enemySet:
                del Xp[e]
            cover.append(key)
            self._solve(friendSet, Xp, cover, covers)
            del X[key]
            #print results
            cover.pop()

    def solve_greedy(self, X):
        universe = self.createUniverse(X)
        return self._solve_greedy(X, universe, [])

    def _solve_greedy(self, X, universe, result):
        if len(X) == 0:
            return result
        else:
            key, value = self.findMaximum(X, universe)
            result.append(key)
            friendSet, enemySet = self.findFriendEnemy(X, key)
            universe = list(set(universe) - set(X[key]))
            Xp = deepcopy(X)
            del Xp[key]
            for val in enemySet:
                del Xp[val]
            return self._solve_greedy(Xp, universe, result)

    def createY(self, X):
        # 1. from X, find universe
        # X = {
        #     'A': [1, 2, 3],
        #     'B': [3, 4],
        #     'C': [4, 5, 6]
        # }
        # create a dictionary from key to [length, select, exclusive]
        # Y = {
        #     'A': [3, set('C'), set('B')]
        #     'B': [2, set(''),  set('A', 'C')]
        #     'C': [3, set('A'), set('B')]
        # universe = set()
        Y = {}
        for i in X:
            #universe |= set(i)
            friendSet, enemySet = self.findFriendEnemy(X, i)
            result = [len(X[i]), friendSet, enemySet]
            Y[i] = result
        #print Y
        #print universe
        return Y
        
    def asolve(self, X):
        Y = self.createY(X)
        self.solutionResults = []
        for y in Y:
            #print "first: add %d" % y
            solutionList = [y]
            f = set(Y[y][1])
            e = set(Y[y][2])
            e.add(y)
            #print f
            res = self._solve(Y, f, e, solutionList)

        #res = sorted(self.solutionResults, key=len)[-1]
        
        max = -1
        result = {}
        #print X
        for solutions in self.solutionResults:
            #print solutions
            
            res = 0
            for i in solutions:
                #print i
                res += len(X[i])
                result[str(solutions)] = res
        res = sorted(result, key=lambda x: -result[x])[0]
            #print X[i]
            # summedResult = sum(X[i])
            # print summedResult
        #print eval(res), len(re)
        # res is a string, so it should be converted into an expression
        return eval(res)
        
    def a_solve(self, Y, friends, enemies, solutionList):
        # global count
        # print count
        # count += 1
        #if count == 10: sys.exit(0)
        if not friends: 
            
            #print "print SOL", solutionList
            self.solutionResults.append(deepcopy(solutionList))
            #print solutionList
            #print self.solutionResults
            return solutionList
        else:
            for y in friends:
                solutionList.append(y)
                #print "add %d" % y
                e = set(Y[y][2])
                e.add(y)
                e |= enemies
                f = set(Y[y][1])
                f -= enemies
                #print f
                res = self._solve(Y, f, e, solutionList)
                #print "OUT"
                #solutionList.remove(y)
                #print res
                solutionList.remove(y)
                #return res
    # def solve(self, X): # , Y, solution = []):
    #     Y = self.createY(X)
    #     selection = sorted(Y, key = lambda x: -Y[x][0])[0]
    #     
    #     f = set(Y[selection][1])
    #     e = set(Y[selection][2])
    #     
    #     friends = f
    #     enemies = e
    #     enemies.add(selection)
    #     
    #     return self._solve(Y, friends, enemies, [selection]) 
    # 
    # def _solve(self, universe, friends, enemies, selectionList):
    #     if not friends: 
    #         return selectionList
    #     else:
    #         Y = {j:universe[j] for j in filter(lambda x: x in friends, universe)}
    #         selection = sorted(Y, key = lambda x: -Y[x][0])[0] # Don't forget the last [0]
    #         f = set(universe[selection][1])
    #         e = set(universe[selection][2])
    #         friends = f
    #         enemies |= e
    #         enemies.add(selection)
    #         friends -= enemies
    #         selectionList.append(selection)
    #         return self._solve(universe, friends, enemies, selectionList)
    
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testMaxCover import *

    unittest.main(verbosity=2)