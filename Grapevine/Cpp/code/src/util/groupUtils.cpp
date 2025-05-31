//
// Created by smcho on 5/30/13.
// Copyright (c) 2013 ___MPC___. All rights reserved.
//
// To change the template use AppCode | Preferences | File Templates.
//

#include "groupUtils.h"

void GroupUtils::getListFromSummary(const ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, std::vector<int>& result)
{
    int groupSize;
    bool res = summary.get(size_key, groupSize);
    if (res == true) {
        for (int i = 0; i < groupSize; i++) {
            int value; 
            res = summary.get(prefix_key + std::to_string(i), value);
            if (res == true)
                result.push_back(value);
            else
                throw Error(__FILE__ + std::to_string(__LINE__));
        }
    }
}
void GroupUtils::addItemIntoSummary(ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, int value)
{
    int size = 0;
    if (summary.containsKey(size_key))
        summary.get(size_key, size);
    
    std::string newKey = prefix_key + std::to_string(size);
    std::vector<int> values;
    getListFromSummary(summary, size_key, prefix_key, values);
    
    if (!Util::in(values, value)) { // value in values:
        summary.put(newKey, value);
        summary.put(size_key, size + 1);
    }
}

void GroupUtils::addItemsIntoSummary(ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, std::vector<int>& values)
{
    for (auto value : values)
        addItemIntoSummary(summary, size_key, prefix_key, value);    
}

void GroupUtils::removePrefix(ContextSummary& summary, const std::string& size_key, const std::string& prefix_key)
{
    int size = 0;
    bool res = summary.get(size_key, size);
    if (res == true) {
        for (int index = 0; index < size; index++)
            summary.remove(prefix_key + std::to_string(index));
        summary.remove(size_key);
    }
}

bool GroupUtils::isMember(const ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, int id)
{
    std::vector<int> items;
    getListFromSummary(summary, size_key, prefix_key, items);
    return Util::in(items, id); //  in items;
}

void GroupUtils::combineMembers(std::vector<int>& member1, const std::vector<int>& member2)
{
    for (auto member : member2) {
        if (!Util::in(member1, member)) // not member in member1:
            member1.push_back(member);
    }
}

void GroupUtils::getDeclaredMemberships(const ContextSummary& summary, std::vector<int>& result)
{
    return getListFromSummary(summary, GROUP_DECLARATIONS_ENUMERATED, GROUP_DECLARATION_PREFIX, result);
}


void GroupUtils::addDeclaredGroupMembership(ContextSummary& summary, int gId)
{
    return addItemIntoSummary(summary, GROUP_DECLARATIONS_ENUMERATED, GROUP_DECLARATION_PREFIX, gId);
}

bool GroupUtils::declaresGroupMembership(const ContextSummary& summary, int gId)
{
    return isMember(summary, GROUP_DECLARATIONS_ENUMERATED, GROUP_DECLARATION_PREFIX, gId);
}

void GroupUtils::addGroupMember(ContextSummary& groupSummary, int gId)
{
    return addItemIntoSummary(groupSummary, MEMBERS_ENUMERATED, MEMBER_PREFIX, gId);
}

/**
 * getGroupMembers returns false when
 *   1. MEMBERS_ENUMERATED is false <- No members
 */
void GroupUtils::getGroupMembers(const ContextSummary& groupSummary, std::vector<int>& members)
{
    return getListFromSummary(groupSummary, MEMBERS_ENUMERATED, MEMBER_PREFIX, members);
}

void GroupUtils::setGroupMembers(ContextSummary& groupSummary, const std::vector<int>& memberIds)
{
    int previousNumberOfMembers;
    groupSummary.get(MEMBERS_ENUMERATED, previousNumberOfMembers);
    
    int newNumberOfMembers = memberIds.size();
    
    for (int i = 0; i < previousNumberOfMembers; i++)
    {
        groupSummary.remove(MEMBER_PREFIX + std::to_string(i));
    }
    //std::cout << groupSummary.to_string() << std::endl;
    groupSummary.put(MEMBERS_ENUMERATED, 0);
    for (auto memberId : memberIds) {
        //std::cout << memberId;
        GroupUtils::addGroupMember(groupSummary, memberId);
        //std::cout << groupSummary.to_string() << std::endl;
    }
}

bool GroupUtils::isAggregated(const ContextSummary& groupSummary, int idToCheck)
{
    return isMember(groupSummary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, idToCheck);
}

bool GroupUtils::haveNoCommonAggregation(const ContextSummary& summary1, const ContextSummary& summary2)
{
    std::vector<int> ids1;
    getAggregatedIds(summary1, ids1);
    std::vector<int> ids2;
    getAggregatedIds(summary2, ids2);
    std::vector<int> result;
    
    Util::andOperation(ids1, ids2, result);
    return (result.size() == 0);
}

void GroupUtils::getAggregatedIds(const ContextSummary& summary, std::vector<int>& result)
{
    return getListFromSummary(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, result);
}

void GroupUtils::addAggregatedId(ContextSummary& summary, int memberId)
{
    return addItemIntoSummary(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, memberId);
}   

void GroupUtils::setAggregatedIds(ContextSummary& summary, std::vector<int>& aggregatedIds)
{
    removePrefix(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX);
    addItemsIntoSummary(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, aggregatedIds);
}
    
void GroupUtils::aggregateIntoGroupSummary(ContextSummary& groupSummary1, const ContextSummary& groupSummary2)
{
    /*    """
    combine all the members and aggregation of group1/group2 into group1
    """ */
    std::vector<int> memberIds1;
    std::vector<int> memberIds2;
    getGroupMembers(groupSummary1, memberIds1);
    getGroupMembers(groupSummary2, memberIds2);
    combineMembers(memberIds1, memberIds2);
    setGroupMembers(groupSummary1, memberIds1);
    
    // Do the same thing with aggregation
    std::vector<int> aggregatedIds1;
    std::vector<int> aggregatedIds2;
    getAggregatedIds(groupSummary1, aggregatedIds1);
    getAggregatedIds(groupSummary2, aggregatedIds2);
    combineMembers(aggregatedIds1, aggregatedIds2);
    setAggregatedIds(groupSummary1, aggregatedIds1);
}

void GroupUtils::updateGroupAggForOneSummary(ContextSummary& groupSummary, const ContextSummary& summary)
{
    int gid = groupSummary.getId();

    if (declaresGroupMembership(summary, gid) || ((summary.getId() == gid) \
       &&  !isAggregated(groupSummary, summary.getId()) \
       && haveNoCommonAggregation(groupSummary, summary)))
       aggregateIntoGroupSummary(groupSummary, summary);
}
        
void GroupUtils::updateGroupAgg(ContextSummary& groupSummary, const std::vector<ContextSummary>& summaries)
{
    for (auto summary : summaries)
        updateGroupAggForOneSummary(groupSummary, summary);
}