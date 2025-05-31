#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "util.h"
#include "contextSummarySerializer.h"

using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class ContextSummarySerializerTest : public QuickTest {
 protected:
  virtual void SetUp() {
      c = new ContextSummarySerializer();
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      delete c;
      QuickTest::TearDown();
  }
  ContextSummarySerializer* c;
};


TEST_F(ContextSummarySerializerTest, writeSummaryReadSummary) {
    std::map<std::string, int> dbx {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    time_t timestamp = 100000;
    ContextSummary* s = new ContextSummary(11, dbx, 10, timestamp);   // pretty short hops
    auto result = c->writeSummary(s);
    //Util::print(result);
    
    //unsigned char ;
    auto recoveredSummary = c->readSummary(); // ch);
    auto s2 = recoveredSummary.get();
    // EXPECT_TRUE(s->getId() == s2->getId());
    // EXPECT_TRUE(s->getHops() == s2->getHops());
    // EXPECT_TRUE(s->getTimestamp() == s2->getTimestamp());
    // EXPECT_TRUE(s->getDb() == s2->getDb());
    
    EXPECT_TRUE(*s == *s2);
}

TEST_F(ContextSummarySerializerTest, writeSummariesReadSummaries) {
    std::map<std::string, int> dbx {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    time_t timestamp = 100000;
    ContextSummary* s = new ContextSummary(11, dbx, 10, timestamp);   // pretty short hops
    
    std::map<std::string, int> dbx2 {
          {"GroupsEnumerated",3},
          {"Group0",100},{"Group1",103},{"Group2",104},
          {"IdsAggregated",3},
          {"Id0",10}, {"Id1",20}, {"Id2",30}};
    time_t timestamp2 = 1000300;
    GroupContextSummary* s2 = new GroupContextSummary(21, dbx2, 100, timestamp2);   // pretty short hops
    
    vector<ContextSummary*> v {s, s2};
    
    auto result = c->writeSummaries(v);

    vector<unique_ptr<ContextSummary>> recoveredSummary = c->readSummaries(); // ch);
    
    int i = 0;
    for (auto&s: recoveredSummary)
    {
        ContextSummary* s2 = v[i];
        EXPECT_TRUE(*s2 == *(s.get()));
        i++;
    }
}
