#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "util.h"
#include "contextSummary.h"
#include "groupContextSummary.h"

using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class GroupUtilsTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
      summary = new ContextSummary(1, db);
      summary2 = new ContextSummary(2, db2);
      summary3 = new ContextSummary(3, db3);
      groupSummary = new GroupContextSummary(101, groupDb);
      groupSummaryNull = new GroupContextSummary(100, groupDbNull);
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
      delete summary;
      delete summary2;
      delete summary3;
      delete groupSummary;
      delete groupSummaryNull;
      result.clear();
  }
  
  std::map<std::string, int> db {
        {"GroupsEnumerated",3},
        {"Group0",101},{"Group1",102},{"Group2",103},
        {"IdsAggregated",5},
        {"Id0",10}, {"Id1",20}, {"Id2",30}, {"Id3",40}, {"Id4",50}};
  std::vector<int> aggregatedIds {10,20,30,40,50};

  std::map<std::string, int> db2 {
        {"GroupsEnumerated",3},
        {"Group0",101},{"Group1",103},{"Group2",104},
        {"IdsAggregated",3},
        {"Id0",10}, {"Id1",20}, {"Id2",30}};
  std::vector<int> aggregatedIds2 {10,20,30};
  
  std::map<std::string, int> db3 {
        {"GroupsEnumerated",3},
        {"Group0",101},{"Group1",104},{"Group2",105},
        {"IdsAggregated",3},
        {"Id0",110}, {"Id1",120}, {"Id2",130}};
  std::vector<int> aggregatedIds3 {110,120,130};
  
  std::map<std::string, int> groupDb {
        {"MembersEnumerated",3},
        {"Member0",1},{"Member1",2},{"Member2",3}};
  std::vector<int> groupSummaryMembers {1,2,3};
  
  std::map<std::string, int> groupDbNull;

  ContextSummary* summary;
  ContextSummary* summary2;
  ContextSummary* summary3;
  GroupContextSummary* groupSummary;
  GroupContextSummary* groupSummaryNull;
  vector<int> result;
};

TEST_F(GroupUtilsTest, getDeclaredMemberships) {
    vector<int> result;
    vector<int> expected {101, 102, 103};
    GroupUtils::getDeclaredMemberships(*summary, result);
    //EXPECT_EQ(res, true);
    //Util::print(result);
    Util::sameTwoVectors(result, expected);
}

TEST_F(GroupUtilsTest, addDeclaredGroupMembership) {
    vector<int> result;
    vector<int> expected {100, 101, 102, 103};
    GroupUtils::addDeclaredGroupMembership(*summary, 100);
    //EXPECT_EQ(res, true);
    //Util::print(result);
    GroupUtils::getDeclaredMemberships(*summary, result);
    //EXPECT_EQ(res, true);
    Util::sameTwoVectors(result, expected);
}

TEST_F(GroupUtilsTest, declaresGroupMembership) {
    bool res = GroupUtils::declaresGroupMembership(*summary, 100);
    EXPECT_EQ(res, false);
    res = GroupUtils::declaresGroupMembership(*summary, 101);
    EXPECT_EQ(res, true);
    res = GroupUtils::declaresGroupMembership(*summary, 102);
    EXPECT_EQ(res, true);
    res = GroupUtils::declaresGroupMembership(*summary, 103);
    EXPECT_EQ(res, true);
}

TEST_F(GroupUtilsTest, addGroupMember) {
    // member is added to group
    GroupUtils::addGroupMember(*groupSummaryNull, 1200);
    //EXPECT_EQ(res, true);
    
    GroupUtils::getGroupMembers(*groupSummaryNull, result);
    std::vector<int> expected {1200};
    //EXPECT_EQ(res, true);
    EXPECT_TRUE(Util::sameTwoVectors(result, expected));
}

TEST_F(GroupUtilsTest, getGroupMembers) {
    GroupUtils::getGroupMembers(*groupSummary, result);
    std::vector<int> expected = groupSummaryMembers;
    //EXPECT_EQ(res, true);
    EXPECT_TRUE(Util::sameTwoVectors(result, expected));
}

TEST_F(GroupUtilsTest, setGroupMembersEmpty) {
    std::vector<int> emptyVector;
    // now group has nothing in it
    GroupUtils::setGroupMembers(*groupSummary, emptyVector);
    GroupUtils::getGroupMembers(*groupSummary, result);
    EXPECT_TRUE(Util::sameTwoVectors(result, emptyVector));
}

TEST_F(GroupUtilsTest, setGroupMembers) {
    std::vector<int> expected = {1,2,3,4,5,6,7,8,9,10};
    // now group has nothing in it
    GroupUtils::setGroupMembers(*groupSummary, expected);
    GroupUtils::getGroupMembers(*groupSummary, result);
    // Util::print(result);
    // Util::print(expected);
    EXPECT_TRUE(Util::sameTwoVectors(result, expected));
}

TEST_F(GroupUtilsTest, isAggregated) {
    EXPECT_TRUE(GroupUtils::isAggregated(*summary, 10));
    EXPECT_FALSE(GroupUtils::isAggregated(*summary, 1000));
}

TEST_F(GroupUtilsTest, haveNoCommonAggregation) {
    EXPECT_FALSE(GroupUtils::haveNoCommonAggregation(*summary, *summary2));
    EXPECT_TRUE(GroupUtils::haveNoCommonAggregation(*summary, *summary3));
}

TEST_F(GroupUtilsTest, getAggregatedIds) {
    GroupUtils::getAggregatedIds(*summary, result);
    EXPECT_TRUE(Util::sameTwoVectors(aggregatedIds, result));
}

TEST_F(GroupUtilsTest, addAggregatedId) {
    int ids;
    summary->get(IDS_AGGREGATED, ids);
    GroupUtils::addAggregatedId(*summary, 200);
    
    // # the ids has the total number:
    // # [1,2,3,4,5] --> 5, but the index is 0,1,2,3,4,*5
    // # So ids should be the newly assigned index
    int value;
    summary->get(ID_AGGREGATION_PREFIX + std::to_string(ids), value);
    
    int ida_plus1;
    summary->get(IDS_AGGREGATED, ida_plus1);
    EXPECT_EQ(ida_plus1, ids + 1);
    EXPECT_EQ(value, 200);
}

TEST_F(GroupUtilsTest, setAggregatedIds) {
    std::vector<int> ids {41,42,43,44,45,46,47};
    GroupUtils::setAggregatedIds(*summary, ids);
    
    int numberOfIds;
    summary->get(IDS_AGGREGATED, numberOfIds);
    EXPECT_EQ(numberOfIds, ids.size());
}

TEST_F(GroupUtilsTest, aggregateIntoGroupSummary) {
    int aggregatedSize1;
    summary->get(IDS_AGGREGATED, aggregatedSize1);
    int aggregatedSize2;
    bool res2 = groupSummary->get(IDS_AGGREGATED, aggregatedSize2);
    
    EXPECT_EQ(aggregatedIds.size(), aggregatedSize1);
    EXPECT_EQ(res2, false);
    
    GroupUtils::aggregateIntoGroupSummary(*groupSummary, *summary);
    groupSummary->get(IDS_AGGREGATED, aggregatedSize2);
    EXPECT_EQ(aggregatedIds.size(), aggregatedSize2);
}

TEST_F(GroupUtilsTest, updateGroupAggForOneSummary) {
    EXPECT_TRUE(GroupUtils::declaresGroupMembership(*summary, groupSummary->getId()));
    EXPECT_FALSE(GroupUtils::isAggregated(*groupSummary, summary->getId()));
    EXPECT_TRUE(GroupUtils::haveNoCommonAggregation(*groupSummary, *summary));
    int aggregatedSize1;
    summary->get(IDS_AGGREGATED, aggregatedSize1);
    int aggregatedSize2;
    bool res2 = groupSummary->get(IDS_AGGREGATED, aggregatedSize2);

    EXPECT_EQ(aggregatedIds.size(), aggregatedSize1);
    EXPECT_EQ(res2, false);
    
    GroupUtils::updateGroupAggForOneSummary(*groupSummary, *summary);
    groupSummary->get(IDS_AGGREGATED, aggregatedSize2);
    EXPECT_EQ(aggregatedIds.size(), aggregatedSize2);
}

TEST_F(GroupUtilsTest, updateGroupAgg) {
    std::vector<ContextSummary> summaries {*summary, *summary2, *summary3};
    GroupUtils::updateGroupAgg(*groupSummary, summaries);
    // TODO - no eq???
}