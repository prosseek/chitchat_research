# http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

X = {1, 2, 3, 4, 5, 6, 7}
Y = {
    'A': [1, 4, 7],
    'B': [1, 4],
    'C': [4, 5, 7],
    'D': [3, 5, 6],
    'E': [2, 3, 6, 7],
    'F': [2, 7]}

def solve(X, Y, solution=[]):
    print "*" * 10, "\nin solve"
    print X, solution
    print 
    
    if not X:
        print "solution, not X", solution
        return list(solution)
    else:
        result = None
        c = min(X, key=lambda c: len(X[c]))
        print "max as c list(X[c])", c, list(X[c])
        for r in list(X[c]):
            print "r", r
            print "list[X[c]]", list(X[c])
            solution.append(r)
            cols = select(X, Y, r)
            result = solve(X, Y, solution)
            print "res from solve:", result
            #for s in solve(X, Y, solution):
            #    return s
            #print X
            print "reverted", r
            deselect(X, Y, r, cols)
            solution.pop()
            print "solution", solution
            
        print "RETURN from else", result
        return result

def select(X, Y, r):
    #print "INX", X
    #print "INY", Y
    cols = []
    for j in Y[r]:
        # print "j", j
        for i in X[j]:
            # print "i", i
            for k in Y[i]:
                # print "k", k
                if k != j: 
                    # print "remove i", i
                    # print "X[k]", X[k],k
                    X[k].remove(i)
                    # print "X[k]", X[k],k
        #print X[j]
        cols.append(X.pop(j))
        #print X
        #print X[j]
    #print "COLS", cols, "R", r, "X", X, "Y", Y
    return cols

def deselect(X, Y, r, cols):
    #print "unset"
    #print "FROM", X
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
    #print "TO", X

X = {j: set(filter(lambda i: j in Y[i], Y)) for j in X}  
#print X

#print filter(lambda i: 1 in Y[i], Y)
                 
#print X, Y
a = solve(X, Y)
print a