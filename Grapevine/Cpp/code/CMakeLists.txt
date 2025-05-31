cmake_minimum_required(VERSION 2.8)
project( grapevine )

#export CC=/usr/bin/clang
#export CXX=/usr/bin/clang++
# cmake -DCMAKE_BUILD_TYPE:STRING=Debug ../code
# ./gv --gtest_filter=Context*

# http://www.cmake.org/Wiki/CMake_Useful_Variables#Compilers_and_Tools
#set(CMAKE_CXX_FLAGS_DEBUG, ON)
#set(CMAKE_CXX_COMPILER "/opt/local/bin/g++-mp-4.8")
#set(CMAKE_CXX_COMPILER "/usr/bin/llvm-g++-4.2")
# http://stackoverflow.com/questions/5334095/cmake-multiarchitecture-compilation
#set(CMAKE_CXX_FLAGS "-std=c++11 -m64")
set(CMAKE_CXX_FLAGS "-std=c++11 -stdlib=libc++ -DGTEST_USE_OWN_TR1_TUPLE=1")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -stdlib=libc++")
# cmake -DCMAKE_OSX_ARCHITECTURES=x86_64

include_directories(/usr/local/include)
include_directories(.)
include_directories(./src)
include_directories(./src/util)
include_directories(./test)
link_directories(/usr/local/lib)
#link_directories(./lib)

set(grapevine_srcs 
    main.cpp 
    
    # bloomier filter code
    src/contextSummary.cpp
    src/groupContextSummary.cpp
    src/groupDefinition.cpp
    src/serializer.cpp
    src/contextHandler.cpp
    src/contextShim.cpp
    src/contextSummarySerializer.cpp
    src/datagramContextShim.cpp
    src/contextShimmedDatagramSocket.cpp
    
    src/util/util.cpp
    src/util/groupUtils.cpp
    src/util/serializerUtils.cpp
    
    # test code
    test/test_groupContextSummary.cc
    test/test_contextSummary.cc
    
    test/test_serializer.cc
    test/test_groupDefinition.cc
    test/test_contextHandler.cc
    test/test_contextShim.cc
    test/test_contextSummarySerializer.cc
    test/test_datagramContextShim.cc
    test/test_contextShimmedDatagramSocket.cc
    
    test/test_util.cc
    test/test_groupUtils.cc
    test/test_error.cc
    test/test_serializerUtils.cc
    test/test_network_broadcasting.cc
    )
    
add_executable(gv ${grapevine_srcs})
target_link_libraries(gv gtest_clang.a)