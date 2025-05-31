//
// Created by smcho on 5/30/13.
// Copyright (c) 2013 ___MPC___. All rights reserved.
//
// To change the template use AppCode | Preferences | File Templates.
//



#ifndef __GROUP_UTILS_H__
#define __GROUP_UTILS_H__

#include <iostream>
#include <list>
#include <set>
#include <algorithm>
#include <vector>
#include <map>
#include <string>

#include "grapevine.h"
#include "contextSummary.h"
#include "util.h"
#include "error.h"

//class GroupContextSummary;
//namespace bloomier {
    
/**
 * Utility class. All of the methods are static to be used 
 * as static function. 
 */

class GroupUtils {
    static void getListFromSummary(const ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, std::vector<int>& result);
    static void addItemIntoSummary(ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, int value);
    static void addItemsIntoSummary(ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, std::vector<int>& values);
    static void removePrefix(ContextSummary& summary, const std::string& size_key, const std::string& prefix_key);
    static bool isMember(const ContextSummary& summary, const std::string& size_key, const std::string& prefix_key, int id);
    // combined result is allocated into values1
    static void combineMembers(std::vector<int>& values1, const std::vector<int>& values2);
    
public:
    static bool declaresGroupMembership(const ContextSummary& summary, int gId);
    static void getDeclaredMemberships(const ContextSummary& summary, std::vector<int>& result);
    static void addDeclaredGroupMembership(ContextSummary& summary, int gId);
    
    static void addGroupMember(ContextSummary& summary, int id);
    static void getGroupMembers(const ContextSummary& summary, std::vector<int>& result);
    static void setGroupMembers(ContextSummary& summary, const std::vector<int>& ids);
    
    static bool isAggregated(const ContextSummary& summary, int idToCheck);
    static bool haveNoCommonAggregation(const ContextSummary& summary1, const ContextSummary& summary2);
    static void getAggregatedIds(const ContextSummary& summary, std::vector<int>& result);
    
    static void addAggregatedId(ContextSummary& summary, int memberId);
    static void setAggregatedIds(ContextSummary& summary, std::vector<int>& aggregatedIds);
    
    static void aggregateIntoGroupSummary(ContextSummary& groupSummary1, const ContextSummary& groupSummary2);
    static void updateGroupAggForOneSummary(ContextSummary& groupSummary, const ContextSummary& summary);
    static void updateGroupAgg(ContextSummary& groupSummary, const std::vector<ContextSummary>& summaries);
};
//}



#endif //__Util_H_