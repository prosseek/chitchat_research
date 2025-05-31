#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "contextSummary.h"
#include "groupContextSummary.h"
#include "groupDefinition.h"

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class GroupDefinitionTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
      
      db = {{"GroupsEnumerated",3},
            {"Group0",100},{"Group1",101},{"Group2",102}};
      summary = new ContextSummary(1, db);
      
      groupDb = {{"MembersEnumerated",3},
      {"Member0",5}, {"Member1",2}, {"Member2",3}}; //  # 1 is not in the member

      groupDb2 = {{"MembersEnumerated",3},
        {"Member0",5}, {"Member1",2}, {"Member2",15}}; // # only 13 is new member
      
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
      delete summary;
  }
  
  std::map<std::string, int> db;
  std::map<std::string, int> groupDb;
  std::map<std::string, int> groupDb2;
  
  ContextSummary* summary;
  GroupContextSummary* g;
};


TEST_F(GroupDefinitionTest, handleContextSummary1) {
    GroupContextSummary* groupSummary = new GroupContextSummary(100, groupDb);
    GroupDefinition* g = new GroupDefinition(500);
    
    std::vector<int> members;
    GroupUtils::getGroupMembers(*groupSummary, members);
    EXPECT_FALSE(Util::in(members, 1));
    g->handleContextSummary(*groupSummary, *summary);
    
    members.clear();
    GroupUtils::getGroupMembers(*groupSummary, members);
    EXPECT_TRUE(Util::in(members, 1));
    
    delete groupSummary;
    delete g;
}


TEST_F(GroupDefinitionTest, handleContextSummary2) {
    GroupContextSummary* groupSummary = new GroupContextSummary(110, groupDb);
    GroupDefinition* g = new GroupDefinition(500);
        
    //    # after the operation, 1 is still "not" in the member, as gid 
    //    # is not one of its groupEnumerated
    std::vector<int> members;
    GroupUtils::getGroupMembers(*groupSummary, members);
    EXPECT_FALSE(Util::in(members, 1));
    g->handleContextSummary(*groupSummary, *summary);
    
    members.clear();
    GroupUtils::getGroupMembers(*groupSummary, members);
    EXPECT_FALSE(Util::in(members, 1));
    
    delete groupSummary;
    delete g;
}


TEST_F(GroupDefinitionTest, handleGroupSummary) {
    GroupContextSummary* currentGroupSummary = new GroupContextSummary(110, groupDb);
    GroupContextSummary* newGroupSummary = new GroupContextSummary(101, groupDb2);
    GroupDefinition* g = new GroupDefinition(500);
    
    std::vector<int> members;
    GroupUtils::getGroupMembers(*currentGroupSummary, members);
    std::vector<int> value({5,2,3});
    EXPECT_TRUE(Util::sameTwoVectors(members, value));
    
    g->handleGroupSummary(*currentGroupSummary, *newGroupSummary);
    members.clear();
    GroupUtils::getGroupMembers(*currentGroupSummary, members);
    std::vector<int> value2({5,2,3, 15});
    EXPECT_TRUE(Util::sameTwoVectors(members, value2));
    
    delete g;
    delete newGroupSummary;
    delete currentGroupSummary;
    //self.assertEqual(sorted([5,2,3,15]), sorted(getGroupMembers(currentGroupSummary)))
}
