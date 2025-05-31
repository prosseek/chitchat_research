#ifndef __CONTEXT_SHIM_H__
#define __CONTEXT_SHIM_H__

#include "contextHandler.h"
#include "contextSummarySerializer.h"

class ContextShim {
    ContextHandler* h;
    ContextSummarySerializer* s;
public:
    ContextShim()
    {
        s = new ContextSummarySerializer();
        h = ContextHandler::getInstance();
    }
    
    ~ContextShim()
    {
        delete s;
    }
    
    ContextHandler* getContextHandlerPtr() {return h;}
    
    /* from the summaries from handler
     * get the serialized data stored in result buffer
     */
    vector<unsigned char> getContextBytes()
    {
        vector<ContextSummary*> summaries = h->getSummariesToSend();
        clearBuffer();
        vector<unsigned char> result = s->writeSummaries(summaries);
        return result;
    }
    
    void clearBuffer()
    {
        s->clearBuffer();
    }
    
    void setResultBuffer(vector<unsigned char>& input)
    {
        s->setResult(input);
    }
    
    /* assume that the buffer is filled, 
     * it transforms the buffer content into summaries
     */
    vector<unique_ptr<ContextSummary>> processContextBytes() // const vector<unsigned char>& buffer)
    {
        vector<unique_ptr<ContextSummary>> summaries = s->readSummaries();
        return summaries;
    }
};
#endif