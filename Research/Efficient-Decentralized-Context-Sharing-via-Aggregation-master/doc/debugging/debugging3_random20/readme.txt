# Graph
![*random20*](./random20.png)

# Result

    Size: based on the steps
    1:94(94) -> (g(0):c(94))
    2:92(186) -> (g(92):c(0))
    3:90(276) -> (g(90):c(0))
    4:45(321) -> (g(45):c(0))
    5:2(323) -> (g(2):c(0))
    6:2(325) -> (g(2):c(0))

    Accuracy: total
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 48.75%
    STEP: 3 -> AVG 71.00%
    STEP: 4 -> AVG 88.25%
    STEP: 5 -> AVG 91.75%
    STEP: 6 -> AVG 95.75%
    Accuracy: agg
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 41.50%
    STEP: 3 -> AVG 65.75%
    STEP: 4 -> AVG 88.25%
    STEP: 5 -> AVG 91.75%
    STEP: 6 -> AVG 95.75%
    Accuracy: single
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 32.50%
    STEP: 3 -> AVG 34.50%
    STEP: 4 -> AVG 35.25%
    STEP: 5 -> AVG 35.25%
    STEP: 6 -> AVG 35.25%

    Maxhops
    [[0, 14, 6, 9, 18], [1, 14, 6, 9, 18], [2, 17, 15, 9, 18], [10, 14, 6, 9, 18], [13, 14, 6, 9, 18], [16, 14, 6, 9, 18], [18, 9, 12, 4, 19], [18, 9, 15, 14, 0], [18, 9, 15, 14, 13], [18, 9, 15, 17, 2], [18, 9, 15, 14, 10], [18, 9, 15, 17, 1], [18, 9, 15, 3, 16], [19, 4, 6, 9, 18]]

    Size: based on the steps
    1:94(94) -> (g(0):c(94))
    2:450(544) -> (g(0):c(450))
    3:601(1145) -> (g(0):c(601))
    4:94(1239) -> (g(0):c(94))
    5:12(1251) -> (g(0):c(12))

    Accuracy: total
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 76.50%
    STEP: 3 -> AVG 96.50%
    STEP: 4 -> AVG 100.00%
    STEP: 5 -> AVG 100.00%
    Accuracy: agg
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 76.50%
    STEP: 3 -> AVG 96.50%
    STEP: 4 -> AVG 100.00%
    STEP: 5 -> AVG 100.00%
    Accuracy: single
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 76.50%
    STEP: 3 -> AVG 96.50%
    STEP: 4 -> AVG 100.00%
    STEP: 5 -> AVG 100.00%

    Maxhops
    [[0, 14, 6, 9, 18], [1, 14, 6, 9, 18], [2, 17, 15, 9, 18], [10, 14, 6, 9, 18], [13, 14, 6, 9, 18], [16, 14, 6, 9, 18], [18, 9, 12, 4, 19], [18, 9, 15, 14, 0], [18, 9, 15, 14, 13], [18, 9, 15, 17, 2], [18, 9, 15, 14, 10], [18, 9, 15, 17, 1], [18, 9, 15, 3, 16], [19, 4, 6, 9, 18]]
    
# Issue
## Not 100% coverage
I can't get 100% in this case. Why?

    Accuracy: agg
    STEP: 1 -> AVG 28.50%
    STEP: 2 -> AVG 41.50%
    STEP: 3 -> AVG 65.75%
    STEP: 4 -> AVG 88.25%
    STEP: 5 -> AVG 91.75%
    STEP: 6 -> AVG 95.75%