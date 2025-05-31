#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "util.h"
#include "contextHandler.h"
#include "contextShim.h"

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class ContextShimTest : public QuickTest {
 protected:
  virtual void SetUp() {
      shim = new ContextShim();
      h = shim->getContextHandlerPtr();
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      delete shim;
      ContextHandler::resetContextHandler();
      QuickTest::TearDown();
  }
  ContextShim* shim;
  ContextHandler* h;
};

TEST_F(ContextShimTest, getContextBytes_and_processContextBytes) {
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
    h->addGroupDefinition(100);
        
    auto res = shim->getContextBytes();
    // Util::print(res);

    auto summaries = shim->processContextBytes();
    // for (auto& s : summaries)
    // {
    //     cout << s.get()->to_string();
    // }
    // two summaries are processed - 11 and 100
    // (11)[10]:{Group0:100,Group1:103,Group2:104,GroupsEnumerated:3,Id0:10,Id1:20,Id2:30,IdsAggregated:3}-(100000)(100)[3]:{Member0:11,Member1:1,Member2:2,MembersEnumerated:3}-(0)
    EXPECT_TRUE(summaries.size() == 2);
}

TEST_F(ContextShimTest, processContextBytes) {

}
