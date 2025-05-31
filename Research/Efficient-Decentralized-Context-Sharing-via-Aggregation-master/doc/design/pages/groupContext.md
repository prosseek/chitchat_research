## GroupContext

The usage format of GroupContext is

    a = Context(1, 10)
    b = Context(2, 20)
    c = Context(3, 30)
    g = GroupContext(20, [a,b,c])
    
The first parameter is the aggregated value(average number in this example), and the second parameter is the list that constructs the 
aggregated value. 

You don't have to calculate the average, as the average will be automatically calculated when
the first argument is `None`. 

    g = GroupContext(None, [a,b,c])