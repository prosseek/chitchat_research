#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>
#include "serializer.h"

using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class SerializerTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
  }
  Serializer* s;
};


TEST_F(SerializerTest, to_string) {
    s = new Serializer(std::string("Hello, world"));
    EXPECT_EQ("[72][101][108][108][111][44][32][119][111][114][108][100]", s->to_string());
    
    string res = s->to_string("YZabcd", hex);
    EXPECT_EQ("[0x59][0x5a][0x61][0x62][0x63][0x64]", res);
}

TEST_F(SerializerTest, setResult) {
    s = new Serializer();
    s->setResult(std::string("Hello, world"));
    EXPECT_EQ("[72][101][108][108][111][44][32][119][111][114][108][100]", s->to_string());
}

TEST_F(SerializerTest, getResultAsString) {
    s = new Serializer();
    s->setResult(std::string("Hello, world"));
    string res = s->getResultAsString();
    res += "d";
    EXPECT_EQ("[72][101][108][108][111][44][32][119][111][114][108][100][100]", s->to_string(res));
}

TEST_F(SerializerTest, getResult) {
    s = new Serializer();
    s->setResult(std::string("Hello, world"));
    vector<unsigned char> vres = s->getResult();
    string res;
    Util::byteArrayToString(vres, res);
    res += "d";
    EXPECT_EQ("[72][101][108][108][111][44][32][119][111][114][108][100][100]", s->to_string(res));
}

TEST_F(SerializerTest, reset) {
    s = new Serializer("Hello, world");
    s->reset();
    string res = s->getResultAsString();
    EXPECT_EQ("", res);
}

TEST_F(SerializerTest, writeObjectDataInt) {
    s = new Serializer();
    int value = 1*(1 << 24) + 2*(1 << 16) + 3*(1 << 8) + 4;
    s->writeObjectData(value);
    vector<unsigned char> res = s->getResult();
    vector<unsigned char> expected {1,2,3,4};
    EXPECT_EQ(res, expected);
}

TEST_F(SerializerTest, writeObjectDataString) {
    s = new Serializer();
    string value = "hello";
    s->writeObjectData(value);
    vector<unsigned char> res = s->getResult();
    
    vector<unsigned char> expected {0x00,0x00,0x00,0x05,0x68,0x65,0x6c,0x6c,0x6f};
    EXPECT_EQ(res, expected);
}

TEST_F(SerializerTest, writeObjectTimestamp) {
    s = new Serializer();
    time_t input = std::time(0);
    s->writeObjectData(input);
    vector<unsigned char> res = s->getResult();
    
    long unsigned int mask[] = {
        0x00000000000000FF,
        0x000000000000FF00,
        0x0000000000FF0000,
        0x00000000FF000000,
        0x000000FF00000000,
        0x0000FF0000000000,
        0x00FF000000000000,
        0xFF00000000000000
    };
    for (int i = 0; i < 8; i++)
    {
        unsigned char expected = static_cast<unsigned char>((input & mask[i]) >> 8*i);
        EXPECT_EQ(expected, res[7 - i]);
    }
}

TEST_F(SerializerTest, readObjectDataInt) {
    s = new Serializer();
    vector<unsigned char> input {1,2,3,4};
    int res;
    s->readObjectData(input, res);
    int expected = 1*(1 << 24) + 2*(1 << 16) + 3*(1 << 8) + 4;
    EXPECT_EQ(res, expected);
}

TEST_F(SerializerTest, readObjectDataString) {
    s = new Serializer();
    string expected = "Hello, world";
    unsigned char c = static_cast<unsigned char>(expected.size());
    //vector<unsigned char> input {0,0,0,c,'H', 'e','l','l','o',',',' ','w','o','r','l','d'};
    vector<unsigned char> input {'H', 'e','l','l','o',',',' ','w','o','r','l','d'};
    string res;
    s->readObjectData(input, res, expected.size());
    EXPECT_EQ(res, expected);
}

TEST_F(SerializerTest, readObjectDataTimestamp) {
    s = new Serializer();
    time_t expected = std::time(0);
    s->writeObjectData(expected);
    vector<unsigned char> input = s->getResult();
    time_t res;
    s->readObjectData(input, res);
    EXPECT_EQ(res, expected);
}

TEST_F(SerializerTest, size) {
    s = new Serializer("1234567890");
    int res = s->size(); 
    
    EXPECT_EQ(10, res);
}
