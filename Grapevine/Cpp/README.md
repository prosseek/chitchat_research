grapevineCpp
============

Implementation of [Grapevine](http://mpc.ece.utexas.edu/research/grapevine) idea in C++ langauge. Check the related paper [Grapevine: Efficient Situational Awareness in Pervasive Computing Environments](http://mpc.ece.utexas.edu/media/uploads/publishing/percom2012_grapevine_wip.pdf).


## How to build
cd build
cmake -DCMAKE_BUILD_TYPE:STRING=Debug ../code

## Selectively executing unit test
    ./gv --gtest_filter=UtilTest.*

Or make and run only the Context* tests

    make && ./gv --gtest_filter=Context*

refer to [stackoverflow]

## Throw errors
C++ doesn't have a good way to point out where the error occurs. Throw Error() object as follows to get the error.

    throw Error(__FILE__ + std::to_string(__LINE__));

## Think
1. We don't copy the map into the ContextSummary now, but it's dangerous not to get all the information in one Summary. 
2. Some things are not clear.
    2.1 Do we make the map into the ContextHandler as reference so that the whole DB is copied when initialized? Or, do we just keep it as it is using pointer?
3. The time stamp is 1 second resolution in C++, and 1/100 second for Python. Which would be better? 
3. The map structure for received summary is {id:ContextSummary}. It may be a better idea to have {id:*ContextSummary}, but I'm not sure if the pointer approach would work. 
4. Interface parameters are confusing, somethings are references and others are pointers 

[stackoverflow]: http://stackoverflow.com/questions/17093772/selectively-executing-unit-tests-with-googletest/17093852#17093852
