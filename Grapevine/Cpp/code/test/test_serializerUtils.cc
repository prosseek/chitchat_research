#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>
#include "util.h"
#include "serializerUtils.h"

using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class SerializerUtilsTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
  }
};


TEST_F(SerializerUtilsTest, intToByteArray) {
    //s = new Serializer("1234567890");
    vector<unsigned char> res = SerializerUtils::intToByteArray(1234); 
    vector<unsigned char> expected {0x00, 0x00, 0x04, 0xD2};
    EXPECT_EQ(expected, res);
    // then other tests.
    
    int value = 1*(1 << 24) + 2*(1 << 16) + 3*(1 << 8) + 4;
    res = SerializerUtils::intToByteArray(value); 
    expected = {0x01, 0x02, 0x03, 0x04};
    EXPECT_EQ(expected, res);
}

TEST_F(SerializerUtilsTest, timestampToByteArray) {
    time_t input = std::time(0);
    vector<unsigned char> res = SerializerUtils::timestampToByteArray(input);
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

TEST_F(SerializerUtilsTest, byteArrayToInt) {
    vector<unsigned char> input {0x01, 0x02, 0x03, 0x04};
    int res = SerializerUtils::byteArrayToInt(input);
    int expect = 1*(1 << 24) + 2*(1 << 16) + 3*(1 << 8) + 4;
    EXPECT_EQ(res, expect);
}

TEST_F(SerializerUtilsTest, byteArrayToTime) {
    vector<unsigned char> input = {0x00, 0x00, 0x00, 0x00, 0x51, 0xbc, 0xdd, 0x2c};
    time_t res = SerializerUtils::byteArrayToInt(input);
    EXPECT_EQ(1371331884, res);
}