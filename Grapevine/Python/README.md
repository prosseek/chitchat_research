# Grapevine Python

[Grapevine] [grapevine] implementation in Python

## Enhancements

1. Simplifying the ContextSummary class hierarchy
    1. Only ContextSummary/GroupContextSummary
2. Make some of the API names clear
    1. writeSummaries/readSummaries instead of "writeObjectData/readObjectData" 
3. Use my own serializer instead of Java library Kryo/ByteStream
    1. Every serialized data is now byte stream (in other words, string). 
    2. We have our own format for the serialization, and we can be smarter
        1. We can use C type string, instead of Pascal type to save more space
        2. We can strip off the first bytes of timestamp data - it will be the same all the time
    3. We can use zip to reduce the size of the byte stream
    4. Can be cross-platform as we use byte stream (string) for payload
4. Remove not used code: observer pattern

## Limitations
1. The network test uses only UDP broadcasting, no TCP/IP networking implemented.
2. No network interface search code implemented, just uses local ip and port.
3. id is just given as number, but we need a feature to assign id based on network.

## Things to consider
1. Do we really need GroupDefinition?
2. How good or bad in using Bloomier Filters
    1. Under what conditions Bloomier Filters shine?
    2. What's the number in size comparison?
3. Why we don't zip the buffer to shrink the size? I tested with simple example to shrink from 180 bytes to 70 bytes.
4. I need to get the cross platform hasher function that will give me the same numbers under all circimstances.

## TODO
1. Serialize bloomier filter
2. Zip the serialize data
3. C++ implementation
4. Design documentation - with beamer

## MIDTERM TODO
1. Using MD5 algorithm, make the hash code generator for grapevine
2. Rewrite the Java code based on the simplified code
3. We need a checker for contextHandler
    1. input: data for contextHandler
    2. output: true/false if the contextHandler data is well organized - group member connection for example.
4. Internal state debugger. We need some debugging environment to trace the inner workings of grapevine

## Research questions
1. The current group formation is good enough? What other strategies?
2. Understand how to network communicate between grapevine devices. Just broadcasting is good? 
3. Do we need special protocol for grapevine network communication? [broadcasting_tcp]

[broadcasting_tcp]: http://stackoverflow.com/questions/31572/broadcast-like-udp-with-the-reliability-of-tcp
[grapevine]: http://mpc.ece.utexas.edu/research/grapevine "Grapevine project"
