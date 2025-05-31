* [2015/08/17]

### Context as a Map

In Scala, contex is a map from String to Any value. 
It is Any because the value can be String, Int, or Tuple. 

    var map: Map[String, Any] = Map(
        "latitude" ->(10, 10, 10, 10),
        "message" -> "Hello",
        "time" ->(11, 11),
        "date" ->(2014, 10, 1))
        
### BloomierFilterSummary

Parameters

* n : is the number of elements
* m : is the table row count
* k : the number of hash functions
* q : the table widht in bits 

The input of create function is map/m/k/q (bit). q controls the folding factor; when q = 8, the width is just one byte. 

    t = new BloomierFilterSummary
    t.create(map = map1, m = 8, k = 3, q = 8*4)

#### Size calculation

`m/8 + n * (q / 8)` is the table size in bytes (excluding the headers). getM() returns  returns M, but the M can be different from the initial M. 

So, the table size in the example is as follows: Disregards all the values, select only the first one. 
    
    t.getM()/8 + 4 * 4
    (17,19,19)
    
The second and third is serialized size, and compressed size, but forget about them for a while, just use getSerializedSize().
    
    width = 1, (25,27,27)
    width = 2, (24,25,25)
    width = 3, (29,30,30)
    width = 4, (29,31,31)
    width = 5, (31,33,33)
    width = 6, (37,39,39)
    width = 7, (36,38,38)
    width = 8, (41,43,43)
    Labeled - (44,52,52)
    
Retrieval data is two step check/get

    if (t.check("latitude") == NoError)) assert(t.get("latitude") == (10,10,10,10))