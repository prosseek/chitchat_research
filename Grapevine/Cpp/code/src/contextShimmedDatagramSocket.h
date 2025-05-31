#ifndef __CONTEXT_SHIMMED_DATAGRAM_SOCKET_H__
#define __CONTEXT_SHIMMED_DATAGRAM_SOCKET_H__

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

#include "datagramContextShim.h"

using namespace std;

class ContextShimmedDatagramSocket
{   
    const int bufferSize = 1024;
    char* buffer; // [bufferSize];
    int sock;
    sockaddr_in addr;
    DatagramContextShim* shim;
public:
    ~ContextShimmedDatagramSocket()
    {
        delete buffer;
        delete shim;
    }
    ContextShimmedDatagramSocket(string ad, int port) {
        buffer = new char[bufferSize];
        shim = new DatagramContextShim();
        
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = inet_addr(ad.c_str());
        
        assert((sock=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP))!=-1);
    }
    
    vector<unsigned char> getSendPacket(const vector<unsigned char>& payLoad)
    {
        return shim->getSendPacket(payLoad);
    }
    pair<vector<unsigned char>, vector<unique_ptr<ContextSummary>>> receive()
    {   
        bind(sock, (struct sockaddr*)&addr, sizeof(addr));
        // if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) == -1)
        // {
        //     perror("Bind error");
        // } 
        
        // Send the message after the bind     
        //pinger("hello");
            
        socklen_t len = sizeof addr;
        if(recvfrom(sock, buffer, bufferSize, 0, (struct sockaddr*)&addr, &len)==-1)
            perror("recvfrom");
                
        //cout << "\nRECEIVE" << buffer; 
                
        if(close(sock) == -1)
            perror("close");
            
        // TODO - not implemented
        return pair<vector<unsigned char>, vector<unique_ptr<ContextSummary>>>();
    }
    
    int send(const string& payLoad)
    {
        vector<unsigned char> buffer;
        Util::stringToByteArray(payLoad, buffer);
        return send(buffer);
    }
    
    int send(const vector<unsigned char>& payLoad)
    {
        int broadcast=1;
        setsockopt(sock, SOL_SOCKET, SO_BROADCAST,
                    &broadcast, sizeof broadcast);
                    
        vector<unsigned char> sendPacket = getSendPacket(payLoad);
        string buffer;
        Util::byteArrayToString(sendPacket, buffer);
        // sendto(sendPacket, (self.addr, self.port));
        int bytes_sent = sendto(sock, buffer.c_str(), sizeof(buffer.c_str()), 0,
                   (struct sockaddr*)&addr, sizeof(addr));
       return bytes_sent;
    }
};

// from socket import *
// 
// from datagramContextShim import *
// 
// class ContextShimmedDatagramSocket(object):
//     def __init__(self, addr, port):
//         self.addr = addr
//         self.port = port
//         self.shim = DatagramContextShim()
//         
//         self.cs = socket(AF_INET, SOCK_DGRAM)
//         self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
//         self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
//         
//     def receive(self):
//         cs = socket(AF_INET, SOCK_DGRAM)
//         try:
//             cs.bind((self.addr, self.port))
//         except:
//             print 'failed to bind'
//             cs.close()
//             raise
//             cs.blocking(0)
// 
//         data = cs.recvfrom(1024) # get 1024 bytes first
//         cs.close()

//         payload, summaries = self.shim.processReceivedPacket(data[0])
//         return (payload, summaries)

#endif