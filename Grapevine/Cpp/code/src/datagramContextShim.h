#ifndef __DATAGRAM_CONTEXT_SHIM_H__
#define __DATAGRAM_CONTEXT_SHIM_H__

#include <memory>
#include <utility>

#include "contextShim.h"
#include "serializerUtils.h"
#include "util.h"

class DatagramContextShim : public ContextShim
{
public:
    DatagramContextShim() : ContextShim() {}
    
    vector<unsigned char> getSendPacket(const vector<unsigned char>& payLoad) {
        // vector<unsigned char> getContextBytes()
        vector<unsigned char> contextBytes = getContextBytes();
        //Util::print(contextBytes); 
        //cout << contextBytes.size();
        
        int payLoadLength = payLoad.size(); 
        vector<unsigned char> payLoadLengthBytes = SerializerUtils::intToByteArray(payLoadLength);
        //til::print(payLoadLengthBytes);
        
        // http://stackoverflow.com/questions/3177241/best-way-to-concatenate-two-vectors
        // payLoadLengthBytes.size() == 4
        vector<unsigned char> result;
        result.reserve(payLoadLengthBytes.size() + payLoadLength + contextBytes.size());
        result.insert(result.end(), payLoadLengthBytes.begin(), payLoadLengthBytes.end());
        result.insert(result.end(), payLoad.begin(), payLoad.end());
        if (contextBytes.size() > 0)
            result.insert(result.end(), contextBytes.begin(), contextBytes.end());
        
        // cout << payLoadLengthBytes.size() + payLoadLength + contextBytes.size() << endl;
        // cout << result.size();
        return result;
    }
    //void getReceivePacket() {}
    pair<vector<unsigned char>, vector<unique_ptr<ContextSummary>>> processReceivedPacket(const vector<unsigned char>& receivedData) {
        vector<unsigned char> payLoadLengthBytes(receivedData.begin(), receivedData.begin() + 4);
        int payLoadLength = SerializerUtils::byteArrayToInt(payLoadLengthBytes);
        
        vector<unsigned char> payLoadBytes(receivedData.begin() + 4, receivedData.begin() + 4 + payLoadLength);
        vector<unsigned char> contextBytes(receivedData.begin() + 4 + payLoadLength, receivedData.end());
        
        // set the contextBytes into the result buffer
        
        vector<unique_ptr<ContextSummary>> summaries = processContextBytes(); // contextBytes);
        
        pair<vector<unsigned char>, vector<unique_ptr<ContextSummary>>> result;
        result = make_pair(payLoadBytes, move(summaries));
        return result;
        // return pair<vector<unsigned char>, vector<unique_ptr<ContextSummary>>>(payLoadBytes, summaries)
    }
};

#endif