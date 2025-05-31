#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "util.h"

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class UtilTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      //std::cout << "Tearing down...\n";
      aList.clear();
      bList.clear();
      aMap.clear();
      QuickTest::TearDown();
  }

  std::vector<int> aList; // = {10, 20, 30, 40};
  std::vector<int> bList;
  std::map<std::string, int> aMap;
};

TEST_F(UtilTest, addAll) {
    std::vector<int> aList = {10, 20, 30, 40}; 
    bList.push_back(100); bList.push_back(200);
    EXPECT_EQ(4, aList.size());
    Util::addAll(aList, bList);
    EXPECT_EQ(6, aList.size());
}

TEST_F(UtilTest, removeAll) {
    aMap["abc"] = 10; aMap["def"] = 120; aMap["xyz"] = 40;
    std::vector<std::string> aList = {"abc", "def"};
    //aList.push_back(10); aList.push_back(20); aList.push_back(30); aList.push_back(40);
    // bList.push_back(10); bList.push_back(20);
    EXPECT_EQ(3, aMap.size());
    Util::removeAll(aMap, aList);
    EXPECT_EQ(1, aMap.size());
    EXPECT_EQ(40, aMap["xyz"]);
}

TEST_F(UtilTest, removeAllVectors) {
    std::vector<int> a = {10,20,30};
    std::vector<int> b = {20,30,40};
    std::vector<int> c = {10};
    Util::removeAll(a, b);
    EXPECT_TRUE(Util::sameTwoVectors(a, c));
}

TEST_F(UtilTest, byteArrayXor1) {
    unsigned char a[] = {0x00, 0xFF, 0xFF};
    unsigned char b[] = {0xFF, 0xFF, 0x00, 0xFF};
    unsigned char expected[] = {0xFF, 0x00, 0xFF};
    Util::byteArrayXor(a, b, 3);
    for (int i = 0; i < 3; i++)
        EXPECT_EQ(a[i], expected[i]);
}

TEST_F(UtilTest, byteArrayXor2) {
    unsigned char a[] =       {0xFF, 0xFF, 0xFF};
    unsigned char b[] = {0x00, 0xFF, 0x00, 0xFF, 0x00};
    unsigned char expected[] = {0x00, 0xFF, 0x00};
    Util::byteArrayXor(a, b + 1, 3);
    for (int i = 0; i < 3; i++)
        EXPECT_EQ(a[i], expected[i]);
}

TEST_F(UtilTest, setInArray) {
    unsigned char a[] =       {0xFF, 0xFF, 0xFF};
    unsigned char b[] = {0x00, 0xFF, 0x00, 0xFF, 0x00};
    unsigned char expected[] = {0xFF, 0x00, 0xFF};
    Util::setInArray(a, b + 1, 3);
    for (int i = 0; i < 3; i++)
        EXPECT_EQ(a[i], expected[i]);
}

TEST_F(UtilTest, getByteSize) {
    unsigned char a[] = {8, 10, 12, 16};
    unsigned char expected[] = {1,2,2,2};

    for (int i = 0; i < sizeof(a)/sizeof(unsigned char); i++)
        EXPECT_EQ(Util::getByteSize(a[i]), expected[i]);
}

TEST_F(UtilTest, inSetTest) {
    // auto s = new SingletonFindingTweaker(null, null);
    std::set<int> values;
    values.insert(10); values.insert(20); values.insert(30);
    EXPECT_TRUE(Util::in(values, 10));
    EXPECT_FALSE(Util::in(values, 50));
}

TEST_F(UtilTest, inVectorTest) {
    // auto s = new SingletonFindingTweaker(null, null);
    std::vector<int> values;
    values.push_back(10); values.push_back(20); values.push_back(30);
    EXPECT_TRUE(Util::in(values, 10));
    EXPECT_FALSE(Util::in(values, 50));
}

TEST_F(UtilTest, deepcopy) {
    // auto s = new SingletonFindingTweaker(null, null);
    std::map<std::string, int> source;
    source["abc"] = 10; source["def"] = 20; source["xyz"] = 30;
    std::map<std::string, int> dest;
    
    //std::cout << dest["abc"] << std::endl;
    
    Util::deepcopy(source, dest);
    source.clear();
    EXPECT_TRUE(dest["abc"] == 10);
    EXPECT_TRUE(dest["def"] == 20);
    EXPECT_TRUE(dest["xyz"] == 30);
}

TEST_F(UtilTest, getKeys) {
    std::map<std::string, int> source;
    source["abc"] = 10; source["def"] = 20; source["xyz"] = 30;
    std::vector<std::string> keys {"abc", "def", "xyz"};
    
    std::vector<std::string> v = Util::getKeys(source);
    EXPECT_TRUE(Util::sameTwoVectors(v, keys));
}

TEST_F(UtilTest, sameTwoVectorsIntTrue) {
    std::vector<int> first {1,2,3};
    std::vector<int> second {1,2,3};
    
    EXPECT_TRUE(Util::sameTwoVectors(first, second));
    // EXPECT_EQ(6, aList.size());
}

TEST_F(UtilTest, sameTwoVectorsIntFalse) {
    std::vector<int> first {1,2,3};
    std::vector<int> second {1,2,5};
    
    EXPECT_FALSE(Util::sameTwoVectors(first, second));
    // EXPECT_EQ(6, aList.size());
}

TEST_F(UtilTest, sameTwoVectorStringTrue) {
    std::vector<std::string> first {"a","b","c"};
    std::vector<std::string> second {"a","b","c"};
    
    EXPECT_TRUE(Util::sameTwoVectors(first, second));
    // EXPECT_EQ(6, aList.size());
}

TEST_F(UtilTest, sameTwoVectorsStringFalse) {
    std::vector<std::string> first {"a","b","c"};
    std::vector<std::string> second {"a","b","d"};
    
    EXPECT_FALSE(Util::sameTwoVectors(first, second));
    // EXPECT_EQ(6, aList.size());
}

TEST_F(UtilTest, to_stringMapString) {
    std::map<std::string, int> m {{"abc",10}, {"def",20}, {"xyz",100}};
    //std::cout << Util::to_string(m);
    EXPECT_EQ("{abc:10,def:20,xyz:100}", Util::to_string(m));
}

TEST_F(UtilTest, to_stringMapStringNull) {
    std::map<std::string, int> m;
    //std::cout << Util::to_string(m);
    EXPECT_EQ("{}", Util::to_string(m));
}

TEST_F(UtilTest, startswith) {
    std::string m("Hello world");
    std::string sub("Hello");
    std::string sub2("no_hello");
    EXPECT_TRUE(Util::startswith(m, sub));
    EXPECT_FALSE(Util::startswith(m, sub2));
}

TEST_F(UtilTest, endswith) {
    // std::string m("Hello world");
    // std::string sub("world");
    // std::string sub2("no_world");
    // EXPECT_TRUE(Util::endswith(m, sub));
    // EXPECT_FALSE(Util::endswith(m, sub2));
}

TEST_F(UtilTest, andOperation) {
    std::vector<int> a {1,2,3,4,5};
    std::vector<int> b {1,2,6,7,8};
    std::vector<int> expected {1,2};
    std::vector<int> res;
    Util::andOperation(a,b,res);
    EXPECT_TRUE(Util::sameTwoVectors(expected, res));
    // std::string m("Hello world");
    // std::string sub("world");
    // std::string sub2("no_world");
    // EXPECT_TRUE(Util::endswith(m, sub));
    // EXPECT_FALSE(Util::endswith(m, sub2));
}

TEST_F(UtilTest, byteToHexString) {
    std::string res = Util::byteToHexString(0xaa);
    EXPECT_EQ(res,"0xaa");
    
    res = Util::byteToHexString(1);
    EXPECT_EQ(res,"0x01");
    
    res = Util::byteToHexString(0);
    EXPECT_EQ(res,"0x00");
    
    res = Util::byteToHexString(255);
    EXPECT_EQ(res,"0xff");
}

TEST_F(UtilTest, byteArrayToString) {
    std::vector<unsigned char> input {104, 101, 108, 108, 111}; 
    std::string result;
    std::string expected = "hello";
    Util::byteArrayToString(input, result);
    EXPECT_EQ(result, expected);
}

TEST_F(UtilTest, stringToByteArray) {
    std::string input = "hello"; 
    std::vector<unsigned char> result;
    std::vector<unsigned char> expected = {104, 101, 108, 108, 111};
    Util::stringToByteArray(input, result);
    EXPECT_EQ(result, expected);
}