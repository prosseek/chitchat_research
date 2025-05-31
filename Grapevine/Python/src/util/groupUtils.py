# public static final int GROUP_ID_OFFSET = 10000;
# public static final String MEMBER_PREFIX = "Member";
# public static final String MEMBERS_ENUMERATED = "MembersEnumerated";
# public static final String GROUP_DECLARATION_PREFIX = "Group";
# public static final String ID_AGGREGATION_PREFIX = "Id";
# public static final String GROUP_DECLARATIONS_ENUMERATED = "GroupsEnumerated";
# public static final String IDS_AGGREGATED = "IdsAggregated";

import sys
import os.path

sys.path.append(os.path.abspath(".."))
from contextSummary import *

GROUP_DECLARATIONS_ENUMERATED = "GroupsEnumerated"
GROUP_DECLARATION_PREFIX = "Group"

MEMBERS_ENUMERATED = "MembersEnumerated"
MEMBER_PREFIX = "Member"

ID_AGGREGATION_PREFIX = "Id"
IDS_AGGREGATED = "IdsAggregated"

###
# Meta utilties
###
def getListFromSummary(summary, size_key, prefix_key):
    """
    For getAggregatedIds/getDeclaredMemberships
    """
    result = []
    groupSize = summary.get(size_key)
    if groupSize is not None:
        for i in range(groupSize):
            result.append(summary.get(prefix_key + str(i)))
    return result

def addItemIntoSummary(summary, size_key, prefix_key, value):
    """
    For addAggregatedId/addDeclaredGroupMembership
    """
    if summary.containsKey(size_key):
        size = summary.get(size_key)
    else:
        size = 0
    
    newKey = prefix_key + str(size)
    values = getListFromSummary(summary, size_key, prefix_key)
    
    #print >> sys.stderr, newKey
    if not value in values:
        summary.put(newKey, value)
        summary.put(size_key, size + 1)
        
def addItemsIntoSummary(summary, size_key, prefix_key, values):
    for value in values:
        addItemIntoSummary(summary, size_key, prefix_key, value)
        
def removePrefix(summary, size_key, prefix_key):
    size = summary.get(size_key)
    if size is not None:
        for index in range(size):
            summary.remove(prefix_key + str(index))
        #summary.put(size_key, 0)
        summary.remove(size_key)
        
def isMember(summary, size_key, prefix_key, id):
    items = getListFromSummary(summary, size_key, prefix_key)
    return id in items;
    
def combineMembers(member1, member2):
    result = []
    for member in member1:
        result.append(member)
        
    for member in member2:
        if not member in member1:
            result.append(member)
    return result
###
# Meta utilties
###

def getDeclaredMemberships(summary):
    return getListFromSummary(summary, GROUP_DECLARATIONS_ENUMERATED, GROUP_DECLARATION_PREFIX)
    
def addDeclaredGroupMembership(summary, gId):
    return addItemIntoSummary(summary, GROUP_DECLARATIONS_ENUMERATED, GROUP_DECLARATION_PREFIX, gId)

def declaresGroupMembership(summary, gId):
    return isMember(summary, GROUP_DECLARATIONS_ENUMERATED, GROUP_DECLARATION_PREFIX, gId)
    
def addGroupMember(groupSummary, gId):
    return addItemIntoSummary(groupSummary, MEMBERS_ENUMERATED, MEMBER_PREFIX, gId)
    
def getGroupMembers(groupSummary):
    return getListFromSummary(groupSummary, MEMBERS_ENUMERATED, MEMBER_PREFIX)
        
def setGroupMembers(groupSummary, memberIds):
    removePrefix(groupSummary, MEMBERS_ENUMERATED, MEMBER_PREFIX)
    addItemsIntoSummary(groupSummary, MEMBERS_ENUMERATED, MEMBER_PREFIX, memberIds)
            
def isAggregated(summary, idToCheck):
    return isMember(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, idToCheck)
    
def haveNoCommonAggregation(summary1, summary2):
    ids1 = getAggregatedIds(summary1)
    ids2 = getAggregatedIds(summary2)
    # http://www.saltycrane.com/blog/2008/01/how-to-find-intersection-and-union-of/
    return len (set(ids1) & set(ids2)) == 0
    
def getAggregatedIds(summary):
    return getListFromSummary(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX)
    
def addAggregatedId(summary, memberId):
    return addItemIntoSummary(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, memberId)
    
def setAggregatedIds(summary, aggregatedIds):
    removePrefix(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX)
    addItemsIntoSummary(summary, IDS_AGGREGATED, ID_AGGREGATION_PREFIX, aggregatedIds)
    
def aggregateIntoGroupSummary(groupSummary1, groupSummary2):
    """
    combine all the members and aggregation of group1/group2 into group1
    """
    memberIds1 = getGroupMembers(groupSummary1)
    memberIds2 = getGroupMembers(groupSummary2)
    memberIds = combineMembers(memberIds1, memberIds2)
    setGroupMembers(groupSummary1, memberIds)
    
    # Do the same thing with aggregation
    aggregatedIds1 = getAggregatedIds(groupSummary1)
    aggregatedIds2 = getAggregatedIds(groupSummary2)
    aggregatedIds = combineMembers(aggregatedIds1, aggregatedIds2)
    setAggregatedIds(groupSummary1, aggregatedIds)

def updateGroupAggForOneSummary(groupSummary, summary):
    """
    WHY??? - totally cryptic
    """
    gid = groupSummary.getId()
    #print declaresGroupMembership(summary, gid)
    if (declaresGroupMembership(summary, gid) or summary.getId() == gid) \
       and not isAggregated(groupSummary, summary.getId) \
       and haveNoCommonAggregation(groupSummary, summary):
        aggregateIntoGroupSummary(groupSummary, summary)
        
def updateGroupAgg(groupSummary, summaries):
    for summary in summaries:
        updateGroupAggForOneSummary(groupSummary, summary)
        
if __name__ == "__main__":
    import os.path
    
    # Hack 
    # The current directory ("src/util") is the top of the sys.path
    # And it will block the correct module finding especially when util.groupUtils are called.
    # By making the current directory to the last item, we enable calling util.groupUtils as
    # "src" will be found before the "src/util"
    sys.path.append(sys.path.pop(0))
    sys.path.append(os.path.abspath("../../test"))
    from testUtil.testGroupUtils import *
    
    unittest.main(verbosity=2)