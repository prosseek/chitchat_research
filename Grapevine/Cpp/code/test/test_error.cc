#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>
#include "error.h"
#include "Util.h"

using namespace std;

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class ErrorTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
  }
};

int value()
{
    std::stringstream ss;
    ss << "Issues at " << __FILE__ << " on line " << __LINE__;
    throw Error(ss.str());
}

int value2()
{
    throw Error(__FILE__ + std::to_string(__LINE__));
}

TEST_F(ErrorTest, raise) {
    //value();
    EXPECT_THROW(value(), Error);
}

TEST_F(ErrorTest, catchMessage) {
    try {
        value();
    }
    catch (const Error& e)
    {
        //EXPECT_TRUE(strcmp("Issues at /Users/smcho/Desktop/grapevineCpp/code/test/test_error.cc on line 34",e.what()) == 0);
        //cout << e.what() << ":" << strlen(e.what()) <<endl;
        EXPECT_TRUE(Util::startswith(e.what(), "Issues at "));
        EXPECT_TRUE(Util::endswith(e.what(), "test_error.cc on line 34"));
    }
}

TEST_F(ErrorTest, raise2) {
    EXPECT_THROW(value2(), Error);
}

TEST_F(ErrorTest, catchMessage2) {
    try {
        value2();
    }
    catch (const Error& e)
    {
        EXPECT_TRUE(Util::endswith(e.what(), "test_error.cc40"));
        // EXPECT_TRUE(strcmp("/Users/smcho/Desktop/grapevineCpp/code/test/test_error.cc40",e.what()) == 0);
        //cout << e.what() << ":" << strlen(e.what()) <<endl;
    }
}