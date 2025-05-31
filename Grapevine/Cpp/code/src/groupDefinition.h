#include <vector>
#include "groupContextSummary.h"
#include "contextSummary.h"

using namespace std;

class GroupDefinition {
    int groupId;
public:
    GroupDefinition(int groupId)
    {
        this->groupId = groupId;
    }
    
    //? map<int, GroupDefinition> <-- ??? in contextHandler methods
    // I needed to add defautl constructor as
    // I got error: no matching function for call to 'GroupDefinition::GroupDefinition()'
    GroupDefinition()
    {
        GroupDefinition(-1);
    }
    
    int getId() const {return this->groupId;}
    
    void handleContextSummary(GroupContextSummary& currentGroupSummary, const ContextSummary& newSummary);
    void handleGroupSummary(GroupContextSummary& currentGroupSummary, const GroupContextSummary& newSummary);
    void handleContextSummary(GroupContextSummary* currentGroupSummary, const ContextSummary* newSummary);
    void handleGroupSummary(GroupContextSummary* currentGroupSummary, const GroupContextSummary* newSummary);
};


