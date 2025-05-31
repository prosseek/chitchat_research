# Graph
![*random15*](./random15.png)

# Symptom

I think there is a bug, as 1 more step is needed when we have only three maximum hops.

    Size: based on the steps
    1:92(92) -> (g(0):c(92))
    2:496(588) -> (g(0):c(496))
    3:384(972) -> (g(0):c(384))
    4:2(974) -> (g(0):c(2))

    Accuracy: agg
    STEP: 1 -> AVG 47.56%
    STEP: 2 -> AVG 98.22%
    STEP: 3 -> AVG 100.00%
    STEP: 4 -> AVG 100.00%
    Accuracy: single
    STEP: 1 -> AVG 47.56%
    STEP: 2 -> AVG 98.22%
    STEP: 3 -> AVG 100.00%
    STEP: 4 -> AVG 100.00%

    Maxhops
    [[8, 6, 0, 12], [12, 0, 7, 8], [12, 0, 7, 14], [14, 7, 0, 12]]

This is the case with aggregate: only 287 information.

    Size: based on the steps
    1:92(92) -> (g(0):c(92))
    2:92(184) -> (g(92):c(0))
    3:89(273) -> (g(89):c(0))
    4:12(285) -> (g(12):c(0))
    5:2(287) -> (g(2):c(0))

    Accuracy: agg
    STEP: 1 -> AVG 47.56%
    STEP: 2 -> AVG 72.44%
    STEP: 3 -> AVG 96.00%
    STEP: 4 -> AVG 100.00%
    STEP: 5 -> AVG 100.00%
    Accuracy: single
    STEP: 1 -> AVG 47.56%
    STEP: 2 -> AVG 64.00%
    STEP: 3 -> AVG 71.56%
    STEP: 4 -> AVG 71.56%
    STEP: 5 -> AVG 71.56%

    Maxhops
    [[8, 6, 0, 12], [12, 0, 7, 8], [12, 0, 7, 14], [14, 7, 0, 12]]

# Debugging
## Why four steps in Single only case?

In step 3, Host 8 sends 14 about the info of 12.
? Why does this make 2 communication count? 

    **** Host 8 **************************
    DB:Single:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)]
    inputDictionary - {2:[(0)(1)(11)(12)]|3:[(0)(9)(10)(11)(12)]|4:[(1)(9)(10)(12)(13)]|6:[(1)(9)(12)(13)]|7:[(1)(9)(10)(11)(12)(13)]|14:[(0)(1)(10)(13)]}
    outputBuffer - Buffer:Singles:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)]
    oldOutputBuffer - Buffer:Singles:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(13)(14)]
    outputDictionary - {2:[]|3:[]|4:[]|6:[]|7:[]|14:[(12)]}
    ***************************************

The thing is that 12 already has the (12) information, but host 8 does not know about it. 

This is because 14 didn't send (12) to (8) - `14:[(0)(1)(10)(13)]`

**I think it's possible situation.**

    **** Host 14 **************************
    DB:Single:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)]
    inputDictionary - {4:[(1)(2)(6)(10)(12)(13)]|5:[(0)(10)(12)(13)]|7:[(1)(10)(12)(13)]|8:[(0)(1)(10)(13)]|9:[(0)(3)(6)(12)(13)]|11:[(0)(2)(3)(10)(12)]}
    outputBuffer - Buffer:Singles:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)]
    oldOutputBuffer - Buffer:Singles:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(13)(14)]
    outputDictionary - {4:[]|5:[]|7:[]|8:[(12)]|9:[]|11:[]}
    ***************************************
    
## Why there are two communication?
    * host [8] *
    has nothing to send to :  2
    has nothing to send to :  3
    has nothing to send to :  4
    has nothing to send to :  6
    has nothing to send to :  7
    (14) received Contexts from (8): [(12)]

    * host [14] *
    has nothing to send to :  4
    has nothing to send to :  5
    has nothing to send to :  7
    (8) received Contexts from (14): [(12)]

I just missed it.

    **** Host 14 **************************
    DB:Single:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)]
    inputDictionary - {4:[(1)(2)(6)(10)(12)(13)]|5:[(0)(10)(12)(13)]|7:[(1)(10)(12)(13)]|8:[(0)(1)(10)(13)]|9:[(0)(3)(6)(12)(13)]|11:[(0)(2)(3)(10)(12)]}
    outputBuffer - Buffer:Singles:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)]
    oldOutputBuffer - Buffer:Singles:[(0)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(13)(14)]
   
                                           VV
    outputDictionary - {4:[]|5:[]|7:[]|8:[(12)]|9:[]|11:[]}
    ***************************************
    
## What about the aggregation case?

### Trace it

Step 1 OK:

    **** Host 9 **************************
    DB:Single:[(1)(2)(9)(10)(11)(14)]
    inputDictionary - {1:[(1)]|2:[(2)]|11:[(11)]|10:[(10)]|14:[(14)]}
    outputBuffer - Buffer:Aggr:<6(1)(2)(9)(10)(11)(14)>
    oldOutputBuffer - Buffer:Singles:[(9)]
    outputDictionary - {1:[<6(1)(2)(9)(10)(11)(14)>]|2:[<6(1)(2)(9)(10)(11)(14)>]|11:[<6(1)(2)(9)(10)(11)(14)>]|10:[<6(1)(2)(9)(10)(11)(14)>]|14:[<6(1)(2)(9)(10)(11)(14)>]}
    ***************************************
    
Step 2:

    **** Host 9 **************************
    DB:Single:[(1)(2)(9)(10)(11)(14)]NPrime:[<3(0)(6)(12)><4(4)(5)(7)(8)><4(4)(5)(6)(13)><4(3)(5)(12)(13)><5(5)(6)(7)(8)(13)>]
    inputDictionary - {1:[<7(1)(3)(5)(9)(11)(12)(13)>]|2:[<8(2)(5)(6)(7)(8)(9)(10)(13)>]|11:[<8(1)(4)(5)(6)(9)(11)(13)(14)>]|10:[<6(0)(2)(6)(9)(10)(12)>]|14:[<7(4)(5)(7)(8)(9)(11)(14)>]}
    outputBuffer - Buffer:Aggr:<11(1)(2)(5)(6)(7)(8)(9)(10)(11)(13)(14)>
    oldOutputBuffer - Buffer:Aggr:<6(1)(2)(9)(10)(11)(14)>
    outputDictionary - {1:[<11(1)(2)(5)(6)(7)(8)(9)(10)(11)(13)(14)>]|2:[]|11:[<11(1)(2)(5)(6)(7)(8)(9)(10)(11)(13)(14)>]|10:[<11(1)(2)(5)(6)(7)(8)(9)(10)(11)(13)(14)>]|14:[<11(1)(2)(5)(6)(7)(8)(9)(10)(11)(13)(14)>]}
    ***************************************

### Find it!
It's the bug in merger.
    NPrime:[<3(0)(6)(12)><4(4)(5)(7)(8)><4(4)(5)(6)(13)><4(3)(5)(12)(13)><5(5)(6)(7)(8)(13)>]
    
    --> <5(5)(6)(7)(8)(13)> is selected when 
    --> <3(0)(6)(12)><4(4)(5)(7)(8)> should have been selected.

## After the fix

    Size: based on the steps
    1:92(92) -> (g(0):c(92))
    2:92(184) -> (g(92):c(0))
    3:90(274) -> (g(90):c(0))
    4:11(285) -> (g(11):c(0))

    Accuracy: agg
    STEP: 1 -> AVG 47.56%
    STEP: 2 -> AVG 72.44%
    STEP: 3 -> AVG 96.00%
    STEP: 4 -> AVG 100.00%
    Accuracy: single
    STEP: 1 -> AVG 47.56%
    STEP: 2 -> AVG 64.00%
    STEP: 3 -> AVG 72.89%
    STEP: 4 -> AVG 72.89%

    Maxhops
    [[8, 6, 0, 12], [12, 0, 7, 8], [12, 0, 7, 14], [14, 7, 0, 12]]