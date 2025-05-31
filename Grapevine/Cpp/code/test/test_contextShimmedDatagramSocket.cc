#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>

#include "contextSummary.h"
#include "contextHandler.h"
#include "contextShimmedDatagramSocket.h"

string BROADCAST_ADDRESS = "192.168.65.255";
int PORT = 4499;

void pinger()
{
//    cout << "IN";
    ContextSummary* summary = new ContextSummary(1);
    summary->put("test value 1", 1);
    summary->put("test value 2", 2);
    
    ContextHandler* h = ContextHandler::getInstance();
    h->moveMyContext(summary);
    
    //auto socket = ContextShimmedDatagramSocket(BROADCAST_ADDRESS, PORT);
    //socket.send("Hello world");
}

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class ContextShimmedDatagramSocketTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
      sock = new ContextShimmedDatagramSocket(BROADCAST_ADDRESS, PORT);
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
      delete sock;
  }
  ContextShimmedDatagramSocket* sock;
};

// pair<vector<unsigned char>, vector<unique_ptr<ContextSummary>>>
// TEST_F(ContextShimmedDatagramSocketTest, broadCasting) {
//     pinger();
//     auto res = sock->receive();
//     //sleep(1);
// 
//     auto payLoad = res.first;
//     auto summaries = move(res.second);
//     Util::print(payLoad);
// }
