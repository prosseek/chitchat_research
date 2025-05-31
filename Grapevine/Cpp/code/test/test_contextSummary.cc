#include <limits.h>
#include <ctime>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "contextSummary.h"
#include "util.h"

//using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class ContextSummaryTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
      m["abc"] = 10;
      m["def"] = 20;
      m["xyz"] = 100;
      c = new ContextSummary(1, m);
      c2 = new ContextSummary(1, m);
  }
  
  virtual void TearDown() {
      delete c;
      delete c2;
  }
  std::map<std::string, int> m;
  ContextSummary* c;
  ContextSummary* c2;
};

TEST_F(ContextSummaryTest, size) {    
    EXPECT_EQ(3, c->size());
}

TEST_F(ContextSummaryTest, keySet) {  
    // We expect to get 3 elements
    std::vector<std::string> keys = c->keySet();
    EXPECT_EQ(3, keys.size());
    // Util::print(keys);
    Util::getKeys(this->m);
    EXPECT_TRUE(Util::sameTwoVectors(keys, Util::getKeys(this->m)));
}

TEST_F(ContextSummaryTest, toString) {
    //std::cout << c->to_string();
    EXPECT_EQ("(1)[3]:{abc:10,def:20,xyz:100}-(0)", c->to_string()); // Util::to_string(this->m));
}

TEST_F(ContextSummaryTest, eq) {
    //std::cout << std::time(0) << std::endl;
    std::time_t t1 = std::time(0);
    //sleep(1); // (2000);
    //std::time_t t2 = std::time(0);
    //std::cout << std::time(0);
    c->setTimestamp(t1);
    c2->setTimestamp(t1);
    // std::cout << c->to_string();
    // std::cout << c2->to_string();
    
    EXPECT_TRUE(*c == *c2);
}

TEST_F(ContextSummaryTest, sameExceptHops) {
    c->setHops(4);
    EXPECT_TRUE(c->sameExceptHops(*c2));
}

TEST_F(ContextSummaryTest, get) {
    int res1;
    c->get("abc", res1);
    int res2 = this->m["abc"];
    EXPECT_TRUE(res1 == res2);
}

TEST_F(ContextSummaryTest, putNewValue) {
    int res1;
    c->put("hello", 11);
    bool res = c->get("hello", res1);
    
    EXPECT_TRUE(res == true);
    EXPECT_TRUE(res1 == 11);
}

TEST_F(ContextSummaryTest, putOverwrite) {
    int res1;
    c->put("abc", 11);
    bool res = c->get("abc", res1);
    
    EXPECT_TRUE(res == true);
    EXPECT_TRUE(res1 == 11);
}

TEST_F(ContextSummaryTest, containsKey) {
    bool res = c->containsKey("abc"); // , res1);
    bool res1 = c->containsKey("hello"); 
    EXPECT_TRUE(res == true);
    EXPECT_TRUE(res1 == false);
}

TEST_F(ContextSummaryTest, remove) {
    bool res = c->containsKey("abc"); // , res1);
    c->remove("abc");
    bool res1 = c->containsKey("abc"); 
    EXPECT_TRUE(res == true);
    EXPECT_TRUE(res1 == false);
}

TEST_F(ContextSummaryTest, getWireCopy) {
    ContextSummary* summary = c->getWireCopy();
    EXPECT_TRUE(summary != c);
    EXPECT_TRUE(*summary == *c);
    delete summary;
}

TEST_F(ContextSummaryTest, incrementHops) {
    int hops = c->getHops();
    c->incrementHops();
    int newHops = c->getHops();
    EXPECT_TRUE(hops == newHops-1);
}

// MORE tests
// 1. check if db is null, what would happen?
