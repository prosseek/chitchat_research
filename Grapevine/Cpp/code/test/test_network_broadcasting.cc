#include <limits.h>
#include <time.h>
#include <gtest/gtest.h>
#include <list>
#include <map>
#include <string>
#include <iostream>
#include <memory>
#include <sys/types.h> 

#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <thread>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <cassert>

#include "util.h"

using namespace std;

int bufferSize = 100;

void pinger(string msg)
{
    sockaddr_in si_me, si_other;
    int s;
    
    assert((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP))!=-1);
    
    int port=4499;
    
    int broadcast=1;
    setsockopt(s, SOL_SOCKET, SO_BROADCAST,
                &broadcast, sizeof broadcast);

    memset(&si_me, 0, sizeof(si_me));
    si_me.sin_family = AF_INET;
    si_me.sin_port = htons(port);
    si_me.sin_addr.s_addr = inet_addr("192.168.65.255");
    
    string buffer = msg;
    //unsigned char buffer[bufferSize] = "hello";
    int bytes_sent = sendto(s, buffer.c_str(), sizeof(buffer.c_str()), 0,
               (struct sockaddr*)&si_me, sizeof(si_me));
    // cout << bytes_sent; 
}

class QuickTest : public testing::Test {
 protected:
  virtual void SetUp() {
  }
  virtual void TearDown() {
  }
};

class NetworkBroadcastingTest : public QuickTest {
 protected:
  virtual void SetUp() {
      QuickTest::SetUp();
  }
  
  virtual void TearDown() {
      QuickTest::TearDown();
  }
};

// TEST_F(NetworkBroadcastingTest, pingTest) {
//     sockaddr_in si_me;
//     char buffer[bufferSize];
//     int s;
// 
//     assert((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP))!=-1);
//     
//     int port=4499;
//     memset(&si_me, 0, sizeof(si_me));
//     si_me.sin_family = AF_INET;
//     si_me.sin_port = htons(port);
//     si_me.sin_addr.s_addr = inet_addr("192.168.65.255");
//     
//     bind(s, (struct sockaddr*)&si_me, sizeof(si_me));
//     // if (bind(s, (struct sockaddr*)&si_me, sizeof(si_me)) == -1)
//     // {
//     //     perror("Bind error");
//     // } 
//     
//     // Send the message after the bind
//     string sendMessage = "hello";
//     pinger(sendMessage);
//         
//     socklen_t len = sizeof si_me;
//     if(recvfrom(s, buffer, bufferSize, 0, (struct sockaddr*)&si_me, &len)==-1)
//         perror("recvfrom");
//             
//     //cout << "\nRECEIVE" << buffer; 
//             
//     if(close(s) == -1)
//         perror("close");
//     string receivedMessage(buffer);
//     EXPECT_TRUE(sendMessage == receivedMessage);
// }

