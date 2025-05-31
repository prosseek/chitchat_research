### [2016/04/19]04:33PM

When we have a type stucture, how can we build up the type.

    -type hour extends Range(size=5, min=0, max=23, signed=false)
    -type minute extends Range(size=6, min=0, max=59, signed=false)
    +type time extends Encoding(hour, minute)
    -type markethour extends hour(min=10, max=18)
    +type "market time" extends time(markethour)

This will make

    class Market_time extends Encoding(
        name = "market time"
        Array[Range](
            new Range(name = "hour", size = 5, min = 10, max =18, signed = false),
            new Range(name = "minute", size = 6, min = 0, max = 59, signed = false)))

Required condition for algorithm.

1. each type should be extended from one of the groups: Rnage/Encoding/Float/String.
2. when the parent is Range, it should specify min, max, size, signed
3. when the parent is a name that inherits from Range directly or indirectly, it should contain assignemnts.
    * a extends b (x = 10, y = 20), b extends (x = 1, y = 2, z = 3) <- OK
    * a extends b (x) <- not OK
3. when the parent is Encoding, it should contain N number of Range types.
4. The name of the Range comes from the children that has Range as parent.
    * abc extends Range (...) => "name" = "abc", ...

The algorithm get the required information

1. type group - Encoding
    * It can be recovered from following the parent nodes
    * "market time" -> time -> Encoding
        * We also know the ranges to find: hour and minute subtypes
2. The contents
    * If it is Encoding, we know the ranges for the encoding (hour, minute).
    * then, we can update the values from the input
        * it can have upto 2 ranges, but it only provides one range
            * we know that make hour's values to update.
3. The contents of the range
    * For the Range group, it finds all the parents.
        * It starts from the type Range, gets all the elements, and overwrites the element if it
          finds some.
        * markethour -> hour(min=10, max=18) (this has the name) -> Range(size=5, signed=false)
        * => Range(name = "hour", min=10, max=18, size=5, signed=false)
