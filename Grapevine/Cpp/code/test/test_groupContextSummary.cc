#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>
#include "util.h"
#include "groupContextSummary.h"

using namespace std;

class QuickTest : public testing::Test {
protected:
    virtual void SetUp() {
    }
    virtual void TearDown() {
    }
};

class GroupContextSummaryTest : public QuickTest {
 protected:
     virtual void SetUp() {
         QuickTest::SetUp();
         
         g = new GroupContextSummary(101, groupDb);
         //g2 = new GroupContextSummary(1, &this->m);
     }

     virtual void TearDown() {
         delete g;
         //delete g2;
     }
     
     std::map<std::string, int> groupDb {
           {"MembersEnumerated",3},
           {"Member0",1},{"Member1",2},{"Member2",3}};
           
     std::vector<int> groupSummaryMembers {1,2,3};
     std::vector<int> m;
     GroupContextSummary* g;
     //GroupContextSummary* g2;
};

TEST_F(GroupContextSummaryTest, to_string) {
    string expected = "G(101)[3]:{Member0:1,Member1:2,Member2:3,MembersEnumerated:3}-(0)";
    //std::cout << g->to_string();
    EXPECT_EQ(g->to_string(), expected);
}

TEST_F(GroupContextSummaryTest, addMemberIds) {
    std::vector<int> ids {11,12,13,14,15};
    std::vector<int> finalResult {11,12,13,14,15,1,2,3};
    
    g->addMemberIds(groupSummaryMembers);
    g->getMemberIds(m);
    EXPECT_TRUE(Util::sameTwoVectors(groupSummaryMembers, m));
    
    g->addMemberIds(ids);

    m.clear();
    g->getMemberIds(m);
    EXPECT_TRUE(Util::sameTwoVectors(finalResult, m));
}