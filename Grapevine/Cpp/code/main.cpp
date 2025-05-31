//
//  main.cpp
//  BloomierFilter
//
//  Created by smcho on 05/30/13.
//  Copyright (c) 2013 ___MPC___. All rights reserved.
//

#include <iostream>
#include <map>
#include <memory>
#include <gtest/gtest.h>

#include "groupContextSummary.h"

using namespace std;

//http://stackoverflow.com/questions/427589/inspecting-standard-container-stdmap-contents-with-gdb
//#define SHOW(X) cout << # X " = " << ((X).get()->to_string()) << endl

void testPrint( map<int, unique_ptr<GroupContextSummary>> & m, int i )
{
    cout <<  m[i].get()->to_string() << endl;
  // SHOW( m[i] );
  // SHOW( m.find(i)->first );
}

void printVector(const vector<int>& m)
{
    for (auto i: m)
    {
        cout << i << ":";
    }
}

int main(int argc,  char ** argv)
{
    std::cout << "Running main() from gtest_main.cc\n";

    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
    
    return 0;
}
