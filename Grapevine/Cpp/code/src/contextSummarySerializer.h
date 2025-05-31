#ifndef __CONTEXT_SUMMARY_SERIALIZER_H__
#define __CONTEXT_SUMMARY_SERIALIZER_H__

#include "serializer.h"
#include "contextSummary.h"
#include "groupContextSummary.h"

#include <typeinfo>
#include <memory>
#include <typeinfo>

class ContextSummarySerializer : public Serializer
{
public:
    virtual ~ContextSummarySerializer() = default;
    ContextSummarySerializer() : Serializer("") {};
    void clearBuffer() 
    {
        reset();
    }
    
    vector<unsigned char> getBuffer()
    {
        return this->result;
    }
    
    vector<unsigned char> writeSummaries(const vector<ContextSummary*>& summaries)
    {
        for (auto& summary: summaries)
        {
            this->writeSummary(summary);
        }
        return result;
    }
    vector<unsigned char> writeSummary(const ContextSummary* summary)
    {
        unsigned char summarySignature = 'C';
        if (typeid(*summary) == typeid(GroupContextSummary)) {
            summarySignature = 'G';
        }
        
        int uid = summary->getId();
        int hops = summary->getHops();
        time_t timestamp = summary->getTimestamp();
        
        int dbSize = summary->size();
        
        writeObjectData(summarySignature);
        writeObjectData(uid);
        writeObjectData(hops);
        writeObjectData(timestamp);
        writeObjectData(dbSize);
        
        auto keySet = summary->keySet();
        for (auto& key : keySet)
        {
            // int keyLength = key.size();
            // writeObjectData(keyLength);
            writeObjectData(key);
            int result;
            summary->get(key, result);
            writeObjectData(result);
        }
        return result;
    }
    
    unique_ptr<ContextSummary> readSummary()
    {
        unsigned char signature;
        autoReadObjectData(signature);
        
        int uid;
        autoReadObjectData(uid);
        int hops;
        autoReadObjectData(hops);         
        time_t timestamp;
        autoReadObjectData(timestamp);
        int dbSize;
        autoReadObjectData(dbSize);
        
        map<string, int> db;
        for (int i = 0; i < dbSize; i++)
        {
            //int stringLength;
            string key;
            autoReadObjectData(key);
            int value;
            autoReadObjectData(value);
            db[key] = value;
        }
        
        ContextSummary* c;
        if (signature == 'C') {
            c = new ContextSummary(uid, db, hops, timestamp);
        } else
        {
            c = new GroupContextSummary(uid, db, hops, timestamp);
        }
        
        return unique_ptr<ContextSummary>(c);
    }
    
    // vector<unique_ptr<ContextSummary>> readSummaries()
    // {
    //     return readSummaries(this->result);
    // }    
    // 
    vector<unique_ptr<ContextSummary>> readSummaries() //const vector<unsigned char>& buffer)
    {
        vector<unique_ptr<ContextSummary>> result;
        int totalBufferLength = size();
        resetBufferPointer();
        
        while (bufferPointer < totalBufferLength)
        {
            auto s = readSummary();
            result.push_back(move(s));
        }
        
        return result;
    }
};

#endif
    