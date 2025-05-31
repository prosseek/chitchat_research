# Exact cover problem (Algorithm X) in Python

[This link](http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html) will give you the source location.

## Input

It has two inputs, the first one is the total space, and the second one is the candidates. 

    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}
        
        
## The usage

The X input should be transformed into a dictionary of index - candidates. 

    X = {j: set(filter(lambda i: j in Y[i], Y)) for j in X}  
    print X
    
    {1: set(['A', 'B']), 
     2: set(['E', 'F']), 
     3: set(['E', 'D']), 
     4: set(['A', 'C', 'B']), 
     5: set(['C', 'D']), 
     6: set(['E', 'D']), 
     7: set(['A', 'C', 'E', 'F'])}
     
Then you can run the solve() method to get the full cover.
                  
    a = solve(X, Y)
    for i in a: print i
    
    ['B', 'D', 'F']
    
## The idea

Start with index that has the shortest length; 1 has 'A' and 'B' that contains it, so choose it. 

    Y = {'A': [1, 4, 7], 'C': [4, 5, 7], 'B': [1, 4], 'E': [2, 3, 6, 7], 'D': [3, 5, 6], 'F': [2, 7]}
    X = {1: set(['A', 'B']), 
         2: set(['E', 'F']), 
         3: set(['E', 'D']), 
         4: set(['A', 'C', 'B']), 
         5: set(['C', 'D']), 
         6: set(['E', 'D']), 
         7: set(['A', 'C', 'E', 'F'])}  
    solution = []
    
![selection A](./selection1.png)

We start from '1' that has the smallest cover, and we start with solution 'A'.
'A' can cover (1,4,7), so when we choose 'A', 1(A,B), 4(A,B,C->C), 7(A,C,E,F->E,F) in column is chosen automatically. 
It says that when we choose 'A', we can't choose 'A','B','C','E','F'. 

        input x: {1: set(['A', 'B']), 2: set(['E', 'F']), 3: set(['E', 'D']), 4: set(['A', 'C', 'B']), 5: set(['C', 'D']), 6: set(['E', 'D']), 7: set(['A', 'C', 'E', 'F'])}
        solution: 'A'

The result is that we remove all except the 'D'. However, we see that 2 is not covered (empty), so the choice of 'A' is wrong. 

        output x: {2: set([]), 3: set(['D']), 5: set(['D']), 6: set(['D'])} 
        return cols: [set(['A', 'B']), set(['C']), set(['E', 'F'])]

We step back, and choose 'B'. 
        
![selection B](./selection2.png)

Same process, and we get new space that doesn't have 'A','B','C' caused by selecting 'B' as a solution. 

    column: [set(['A', 'B']), set(['C'])] 
    output X: {
        2: set(['E', 'F']), 
        3: set(['E', 'D']), 
        5: set(['D']), 
        6: set(['E', 'D']), 
        7: set(['E', 'F'])} 
        
In a new world, 5 has smallest candidates to cover this: 'D'. So, select 'D'. 

![selection D](./selection3.png)

Now, we have the solution:

![selection F](./selection4.png)

The result shows we have complete cover.

![Result](./result.png)

## Implementation

### Input convertor
Starting from the first element in the total space, find the candidates that contain it. 

    X = {j:DO_SOMETHING for j in X} 
    
The filter selects from Y only the elements appropriate. The rule is to find key (dictionary uses keys) that has j as the value.

    print filter(<lambda i: 1 in Y[i]>, Y) --> ['A', 'B']
    
    DO_SOMETHING:
        set(filter(lambda i: j in Y[i], Y))
        
### selector

![steps](./a.png)

    def select(X, Y, r):
        cols = []
        
It iterates over all the candidates in the solution space

        # X = {1: set(['A', 'B']), 
        # Y = {'A': [1, 4, 7], 'C': [4, 5, 7], 'B': [1, 4], 'E': [2, 3, 6, 7], 'D': [3, 5, 6], 'F': [2, 7]} 
        for j in Y[r]: # candidates r = 'A', Y['A'] = 1/4/7
                     
I need to remove all the columns in X: `X.pop(j)` is needed. It reduces the problem world. 
However, the column contents should not be duplicated: 
        
It also iterates over the total space: candidate covers 1/4/7, so `if k != j: X[k].remove(i)` is needed.

            for i in X[j]: # X[1] - 'A','B'
                for k in Y[i]: # again 1/4/7, but this time 1 is skipped 
                    if k != j: 
                        # X[k] column is modified, and removed all the candidates
                        # remove i A
                        # X[k] set(['A', 'C', 'B']) 4
                        # X[k] set(['C', 'B']) 4
                        # X[k] set(['A', 'C', 'E', 'F']) 7
                        # X[k] set(['C', 'E', 'F']) 7
                        # X[k].remove(i) 
                        # remove i B
                        # X[k] set(['C', 'B']) 4
                        # X[k] set(['C']) 4
                        # For 7, there is no element B so skip it.
            cols.append(X.pop(j)) # Remove the column of 1/4/7
        return cols

### de-selector
This does exactly reversing action of reverse.

    def deselect(X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

        
### Solver

Solver has recursive structure with X as smaller space as we delve into methods. 
When X = [], we return (yield) the values

    if not X:
        yield list(solution)

Otherwise, we start from the minimum sized set.

    c = min(X, key=lambda c: len(X[c])) # key that has the minimum number of elements in a dictionary
    for r in list(X[c]):
    
The idea is to assume the r as the solution, if not we need revert it. 

        solution.append(r) 
        
Use select() method to find columns that contains r. 
        
        cols = select(X, Y, r)
        
Then, we recursively call solve with smaller spaces. 
        
        for s in solve(X, Y, solution):
            yield s
            
Then we unselect and pop when we are done. 

        deselect(X, Y, r, cols)
        solution.pop()    
