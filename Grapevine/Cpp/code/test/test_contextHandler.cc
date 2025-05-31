#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include "groupUtils.h"
#include "contextSummary.h"
#include "contextHandler.h"

using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
  ContextHandler* h;
};

class ContextHandlerTest : public QuickTest {
 protected:
     virtual void SetUp() {
         QuickTest::SetUp();
         summary = new ContextSummary(1, db);
         summary2 = new ContextSummary(2, db2);
         h = ContextHandler::getInstance();
         // summary3 = new ContextSummary(3, &db3);
         // groupSummary = new GroupContextSummary(101, &groupDb);
         // groupSummaryNull = new GroupContextSummary(100, &groupDbNull);
     }

     virtual void TearDown() {
         QuickTest::TearDown();
         delete summary;
         delete summary2;
         // delete summary3;
         // delete groupSummary;
         // delete groupSummaryNull;
         result.clear();
         ContextHandler::resetContextHandler();
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
     ContextSummary* summary;
     ContextSummary* summary2;
     vector<int> result;
};

TEST_F(ContextHandlerTest, moveMyContext) {
    // The summary is automatically destroyed, so it should be
    // 1. pointer (otherwise, it will cause an error as the allocated value will be already gone)
    // 2. forget about the summary, it's not mine anymore
    std::map<std::string, int> db {
           {"GroupsEnumerated",3},
           {"Group0",101},{"Group1",102},{"Group2",103},
           {"IdsAggregated",5},
           {"Id0",10}, {"Id1",20}, {"Id2",30}, {"Id3",40}, {"Id4",50}};
    ContextSummary* summary = new ContextSummary(1, db);
    
    std::map<std::string, int> db2 {
           {"GroupsEnumerated",3},
           {"Group0",101},{"Group1",102},{"Group2",103},
           {"IdsAggregated",5},
           {"Id0",10}, {"Id1",20}, {"Id2",30}, {"Id3",40}, {"Id4",50}};
    ContextSummary* summary2 = new ContextSummary(2, db2);
    
    h->moveMyContext(*summary);
    EXPECT_TRUE(summary == h->getMyContext());
    
    h->moveMyContext(*summary2);
    EXPECT_TRUE(summary2 == h->getMyContext());
    
    // delete summary; // <-- This will raise an error 
} 

TEST_F(ContextHandlerTest, moveReceivedSummaries) {

    map<int, unique_ptr<ContextSummary>> summaries;
	auto s = unique_ptr<ContextSummary>(new ContextSummary(*summary));
        
    summaries[1] = move(s);
    
	h->moveReceivedSummaries(summaries);
    auto res = h->moveReceivedSummaries();
    EXPECT_TRUE(*summary == *res[1].get());
}

TEST_F(ContextHandlerTest, getInstance) {
    ContextHandler* c1 = ContextHandler::getInstance();
    ContextHandler* c2 = ContextHandler::getInstance();
    EXPECT_EQ(c1, c2);
}

TEST_F(ContextHandlerTest, setupGroupDefinitionByMoving) {
    auto g = new GroupDefinition(100);
    auto g2 = h->setupGroupDefinitionByMoving(*g); // setup parameter is always reference
    
    EXPECT_TRUE(g == g2);
    
    auto d = h->getGroupDefinition(100);
    EXPECT_TRUE(d != NULL);
    auto e = h->getGroupContextSummary(100);
    EXPECT_TRUE(d != NULL);
    
    d = h->getGroupDefinition(101);
    EXPECT_TRUE(d == NULL);
    e = h->getGroupContextSummary(101);
    EXPECT_TRUE(d == NULL);
    
    // You should not free the g, as it's owned by the handler.
    // delete g;
    // --> gv(7163) malloc: *** error for object 0x10d509830: pointer being freed was not allocated
}

TEST_F(ContextHandlerTest, setupGroupDefinition) {
    auto groupPtr = h->setupGroupDefinition(100);
    
    auto d = h->getGroupDefinition(100);
    EXPECT_TRUE(d == groupPtr);
    auto e = h->getGroupContextSummary(100);
    EXPECT_TRUE(d != NULL);
    
    d = h->getGroupDefinition(101);
    EXPECT_TRUE(d == NULL);
}

TEST_F(ContextHandlerTest, addGroupDefinitionByMoving) {

    std::map<std::string, int> db {
           {"GroupsEnumerated",3},
           {"Group0",100},{"Group1",101},{"Group2",102},
           {"IdsAggregated",5},
           {"Id0",10}, {"Id1",20}, {"Id2",30}, {"Id3",40}, {"Id4",50}};
    ContextSummary* summary = new ContextSummary(1, db);
    
    std::map<std::string, int> db2 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* summary2 = new ContextSummary(2, db2);
    
    h->copyMyContext(*summary); 
    EXPECT_TRUE(summary != h->getMyContext());
    delete summary;
    
    // 1. set myContext as summary(id 1)
    summary = new ContextSummary(1, db);
    h->moveMyContext(*summary);
    EXPECT_TRUE(summary == h->getMyContext());
    
    // 2. received summaries 
    map<int, unique_ptr<ContextSummary>> receivedSummaries;
    auto copiedSummary = new ContextSummary(*summary2);
    receivedSummaries[2] = unique_ptr<ContextSummary>(copiedSummary);
    h->moveReceivedSummaries(receivedSummaries); // {22:self.summary2})
    EXPECT_TRUE(h->getReceivedSummary(2) == copiedSummary);
    EXPECT_TRUE(h->getReceivedSummary(12) == NULL);
    
    // 3. make group with id 100
    auto g = new GroupDefinition(100); 
    EXPECT_TRUE(h->getGroupContextSummary(100) == NULL);
    h->addGroupDefinitionByMoving(g); // <------ 
    EXPECT_TRUE(h->getGroupContextSummary(100) != NULL);
    
    // check if group 100 has member 1
    vector<int> members;
    GroupContextSummary* gs = h->getGroupContextSummary(100);
    GroupUtils::getGroupMembers(*gs, members);
    // Util::print(members);
    EXPECT_TRUE(Util::in(members, 1)); // 1 is a member -> From context summary
    EXPECT_TRUE(Util::in(members, 2)); // 2 is also a member -> from received summary
}

TEST_F(ContextHandlerTest, performGroupFormations) {
    // I skip the unit test now, as addGroupDefinitionByMoving
    // calls performGroupFormations
}

TEST_F(ContextHandlerTest, moveGroupDefinitions) {
    auto g = new GroupDefinition(100);
    map<int, unique_ptr<GroupDefinition>> gd;
    gd[100] = unique_ptr<GroupDefinition>(g);
    h->moveGroupDefinitions(gd);
    auto g2 = h->getGroupDefinition(100);
    EXPECT_TRUE(g2->getId() == 100);
}

TEST_F(ContextHandlerTest, updateLocalSummaryByMoving) {
    std::map<std::string, int> db {
           {"GroupsEnumerated",3},
           {"Group0",100},{"Group1",101},{"Group2",102},
           {"IdsAggregated",5},
           {"Id0",10}, {"Id1",20}, {"Id2",30}, {"Id3",40}, {"Id4",50}};
    ContextSummary* summary = new ContextSummary(1, db);
    
    h->moveMyContext(summary);
    
    auto c = h->getMyContext();
    EXPECT_TRUE(c->getId() == 1);
    
    std::map<std::string, int> db2 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* summary2 = new ContextSummary(2, db2);
    h->updateLocalSummaryByMoving(summary2);
    
    c = h->getMyContext();
    EXPECT_TRUE(c->getId() == 2);
    // TODO
    // for (auto& groupDefiniton: groupDefinitions)
    // {
    // This part is not tested.
}

TEST_F(ContextHandlerTest, removeLocalSummary) {
    std::map<std::string, int> db {
           {"GroupsEnumerated",3},
           {"Group0",100},{"Group1",101},{"Group2",102},
           {"IdsAggregated",5},
           {"Id0",10}, {"Id1",20}, {"Id2",30}, {"Id3",40}, {"Id4",50}};
    ContextSummary* summary = new ContextSummary(1, db);
    
    h->moveMyContext(summary);
    auto c = h->getMyContext();
    EXPECT_TRUE(c->getId() == 1);
    
    h->removeLocalSummary();
    c = h->getMyContext();
    EXPECT_TRUE(c == NULL);
}

TEST_F(ContextHandlerTest, handleIncomingSummaries) {
    std::map<std::string, int> dbx {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* s = new ContextSummary(11, dbx, 10, 100000);   // pretty short hops
    h->moveMyContext(s);
    
    // 1. setup the existing summary
    std::map<std::string, int> dba1 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* summaryA = new ContextSummary(1, dba1, 10, 100000);   // pretty short hops
    
    std::map<std::string, int> dba2 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* summaryB = new ContextSummary(2, dba2, 10, 100000);   // pretty long hops
    
    std::map<int, unique_ptr<ContextSummary>> summaryMap;
    summaryMap[1] = unique_ptr<ContextSummary>(summaryA);
    summaryMap[2] = unique_ptr<ContextSummary>(summaryB);
    h->moveReceivedSummaries(summaryMap);
    
    // setup the incomming summaries
    std::map<std::string, int> db1 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* summary1 = new ContextSummary(1, db2, 1, 100005);   // new time <- select
    
    std::map<std::string, int> db2 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    ContextSummary* summary2 = new ContextSummary(2, db2, 2, 100000);   // short hops <- select
    
    std::vector<unique_ptr<ContextSummary>> receivedSummaries;
    receivedSummaries.push_back(unique_ptr<ContextSummary>(summary1));
    receivedSummaries.push_back(unique_ptr<ContextSummary>(summary2));
    
    // make group 100
    h->addGroupDefinition(100);
    
    // only summary 1 should be updated
    h->handleIncomingSummaries(receivedSummaries);
    // auto g1 = h->get(1);
    // auto g2 = h->get(2);
    // 
    // cout << g1->getHops(); 
    // cout << g2->getHops(); 
    // EXPECT_TRUE(g1->getHops() == 2);
    // EXPECT_TRUE(g2->getHops() == 3);
    //TODO
    // Need more tests with strategy
}