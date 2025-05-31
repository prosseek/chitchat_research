#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>
#include "datagramContextShim.h"

#include "util.h"

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class DatagramContextShimTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
      shim = new DatagramContextShim();
      h = shim->getContextHandlerPtr();
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
      delete shim;
      ContextHandler::resetContextHandler();
  }
  DatagramContextShim* shim;
  ContextHandler* h;
};


TEST_F(DatagramContextShimTest, getSendPacketNoContext) {
    shim->clearBuffer();
    vector<unsigned char> payLoad {0xa, 0xb, 0xc};
    vector<unsigned char> packet = shim->getSendPacket(payLoad);
    EXPECT_EQ(3 + 4, packet.size());
}

TEST_F(DatagramContextShimTest, getSendPacketWithContextAndprocessReceivedPacket) {
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
    
    vector<unsigned char> payLoad {0xa, 0xb, 0xc};
    vector<unsigned char> packet = shim->getSendPacket(payLoad);
    //Util::print(packet);
    
    auto result = shim->processReceivedPacket(packet);
    auto payLoadResult = result.first;
    auto summaries = move(result.second); // !!! move is needed 
    EXPECT_TRUE(payLoadResult == payLoad);
    
    // there should be two summaries
    // for (auto& summary: summaries)
    // {
    //     cout << summary.get()->to_string();
    // }
    EXPECT_TRUE(summaries.size() == 2);
}

// TEST_F(DatagramContextShimTest, processReceivedPacket) {
// 
// }