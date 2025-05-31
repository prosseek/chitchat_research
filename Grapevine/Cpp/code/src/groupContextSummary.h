#ifndef __GROUP_CONTEXT_SUMMARY_H__
#define __GROUP_CONTEXT_SUMMARY_H__

#include <string>
#include <map>
#include <ctime>
#include <cstddef>
#include <vector>

#include "groupUtils.h"

class GroupContextSummary : public ContextSummary {
    
public:
    // http://stackoverflow.com/questions/120876/c-superclass-constructor-calling-rules
    // GroupContextSummary(int id, int hops = 3, std::time_t timestamp = 0) : \
    //     ContextSummary(id, hops, timestamp) {}
    GroupContextSummary(int id) : \
        ContextSummary(id) {} // , db, hops, timestamp) {}
        
    GroupContextSummary(int id, const std::map<std::string, int>& db, int hops = 3, std::time_t timestamp = 0) : \
        ContextSummary(id, db, hops, timestamp) {}
    GroupContextSummary(const GroupContextSummary& other) : \
        ContextSummary(other) {}
    GroupContextSummary() : GroupContextSummary(-1) {
    }
        
    std::string to_string() const
    {   
        return "G" + ContextSummary::to_string();
    }
    
    void getMemberIds(std::vector<int>& result) const
    {
        return GroupUtils::getGroupMembers(*this, result);
    }
    
    void setGroupMembers(const std::vector<int>& ids)
    {
        return GroupUtils::setGroupMembers(*this, ids);
    }
    void addMemberId(int id)
    {
        return GroupUtils::addGroupMember(*this, id);
    }
    void addMemberIds(const std::vector<int>& ids);
            
    GroupContextSummary* getGroupCopy()
    {
        // Is this safe?
        // http://www.cplusplus.com/doc/tutorial/typecasting/
        ContextSummary* res = getCopy();
        return reinterpret_cast<GroupContextSummary*>(res);
    }
};

#endif