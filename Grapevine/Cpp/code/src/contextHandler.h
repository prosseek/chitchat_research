#ifndef __CONTEXT_HANDLER_H__
#define __CONTEXT_HANDLER_H__

#include <cstddef>
#include <map>
#include <vector>
#include <memory>

#include "groupDefinition.h"
#include "contextSummary.h"
#include "grapevine.h"


class ContextHandler {
    // """
    // It's a singleton, so it should be invoked with ConstextHandler.getInstance()
    // """
    int tau = 3;
    static ContextHandler* singleton; // = nullptr;
    map<int, unique_ptr<GroupDefinition>> groupDefinitions;
    map<int, unique_ptr<GroupContextSummary>> groupContextSummaries;
    map<int, unique_ptr<ContextSummary>> receivedSummaries;
    unique_ptr<ContextSummary> myContext; // = NULL; // unique_ptr<ContextSummary>(NULL);
protected:  
    // Need unit test
    // destructor removes all the allocated pointers, and reset the map
    template <typename T>
    void resetDictionary(map<int, unique_ptr<T>>& m)
    {
        int size = m.size();
        for (auto& val: m) 
        {
            val.second.reset();
        }
        m.clear();
    }

    template<typename T>
    T* getFromMap(map<int, unique_ptr<T>>& m, int gid)
    {
        if (m.find(gid) != m.end()) {
            return m[gid].get();
        }
        return reinterpret_cast<T*>(NULL);
    }
public:    
    void resetAllSummarydata()
    {
        removeLocalSummary();
        resetDictionary<GroupContextSummary>(groupContextSummaries);
        resetDictionary<GroupDefinition>(groupDefinitions);
        resetDictionary<ContextSummary>(receivedSummaries);
    }
    
    ~ContextHandler()
    {
        resetAllSummarydata();
    }
    ////////////////////////////
    
    ContextHandler()
    {
        
    }
    
    // Singleton implementation
    // TODO - Think this is the best implementation
    static ContextHandler* getInstance()
    {
        if (ContextHandler::singleton == nullptr)
        {
            ContextHandler::singleton = new ContextHandler();
        }
        return ContextHandler::singleton;
    }
    
    static void resetContextHandler()
    {
        if (ContextHandler::singleton != nullptr)
        {
            delete ContextHandler::singleton;
        }
        ContextHandler::singleton = nullptr;
    }
    
    void setTau(int tau) {this->tau = tau;}
    int getTau() {return this->tau;}
    
    void moveReceivedSummaries(map<int, unique_ptr<ContextSummary>>& receivedSummaries)
    {
        this->receivedSummaries = move(receivedSummaries);
    }
    void moveGroupContextSummaries(map<int, unique_ptr<GroupContextSummary>>& groupContextSummaries)
    {
        this->groupContextSummaries = move(groupContextSummaries);
    }
    void moveGroupDefinitions(map<int, unique_ptr<GroupDefinition>>& groupDefinitions)
    {
        this->groupDefinitions = move(groupDefinitions);
    }
    
    map<int, unique_ptr<ContextSummary>> moveReceivedSummaries()
    {
        return move(this->receivedSummaries);
    }  
    map<int, unique_ptr<GroupContextSummary>> moveGroupContextSummaries()
    {
        return move(this->groupContextSummaries);
    }
    map<int, unique_ptr<GroupDefinition>> moveDefinitions()
    {
        return move(this->groupDefinitions);
    }
    
    GroupDefinition* getGroupDefinition(int gid) // , GroupDefinition& result)
    {
        return getFromMap<GroupDefinition>(groupDefinitions, gid);
    }
    GroupContextSummary* getGroupContextSummary(int gid) // , GroupContextSummary* & result)
    {
        return getFromMap<GroupContextSummary>(groupContextSummaries, gid);
    }
    ContextSummary* getReceivedSummary(int gid) // , GroupContextSummary* & result)
    {
        return getFromMap<ContextSummary>(receivedSummaries, gid);
    }
    
    
    vector<unique_ptr<ContextSummary>> copyValues(const map<int, unique_ptr<ContextSummary>>& receivedSummaries)
    {
        // get values from summary
        vector<unique_ptr<ContextSummary>> result;
        for (auto& items: receivedSummaries)
        {
            result.push_back(unique_ptr<ContextSummary>(new ContextSummary(*items.second.get())));
        }
        return result;
    }
    
    void performGroupFormations(map<int, unique_ptr<GroupDefinition>>& groupDefinitions, 
                                map<int, unique_ptr<ContextSummary>>& summaries)
    {
        auto values = copyValues(summaries);
        performGroupFormations(groupDefinitions, values);
    }
                                
    void performGroupFormations(map<int, unique_ptr<GroupDefinition>>& groupDefinitions, 
                                vector<unique_ptr<ContextSummary>>& summaries)                            
    {
        // iterate over all the group definitions
        for (auto& gd: groupDefinitions)
        {
            int gid = gd.second->getId();
            GroupContextSummary* groupSummary = getGroupContextSummary(gid);
            
            for (auto& summary: summaries)
            {
                int uid = summary->getId();
                if (gid == uid)
                {
                    gd.second->handleGroupSummary(*groupSummary, 
                       static_cast<GroupContextSummary&>(*summary.get()));
                }
                else 
                {
                    gd.second->handleContextSummary(*groupSummary, *summary.get());
                }
            }
        }
    }
    
    GroupDefinition* setupGroupDefinition(int gId)
    {
        groupContextSummaries[gId] = unique_ptr<GroupContextSummary>(new GroupContextSummary(gId));
        groupDefinitions[gId] = unique_ptr<GroupDefinition>(new GroupDefinition(gId));
        return groupDefinitions[gId].get(); 
    }
    
    GroupDefinition* setupGroupDefinitionByMoving(GroupDefinition& groupDefinition)
    {
        int gId = groupDefinition.getId();
        GroupContextSummary* newGroupSummary = new GroupContextSummary(gId);
        groupContextSummaries[gId] = unique_ptr<GroupContextSummary>(newGroupSummary);
        groupDefinitions[gId] = unique_ptr<GroupDefinition>(&groupDefinition);
        return groupDefinitions[gId].get(); // return the pointer of groupdefinition
    }
    
    GroupDefinition* setupGroupDefinitionByMoving(GroupDefinition* groupDefinition)
    {
        setupGroupDefinitionByMoving(*groupDefinition);
        //TOOD check correct return value
        return groupDefinition;
    }
    
    void addGroupDefinition(int gId)
    {
        GroupDefinition* gd = setupGroupDefinition(gId); // 
        // duplicate code 
        // TODO - remove it later
        GroupContextSummary* groupSummary = getGroupContextSummary(gId);

        ContextSummary* myContext = getMyContext();
        
        if (myContext != NULL) 
        {
            gd->handleContextSummary(groupSummary, myContext);
        }
        performGroupFormations(groupDefinitions, receivedSummaries);
    }
    
    void addGroupDefinitionByMoving(GroupDefinition* groupDefinition)
    {
        addGroupDefinitionByMoving(*groupDefinition);
    }
    
    void addGroupDefinitionByMoving(GroupDefinition& groupDefinition)
    {
        int gId = groupDefinition.getId();
        //cout << "***" << gId << endl;
        GroupDefinition* gd = setupGroupDefinitionByMoving(groupDefinition);
        
        auto groupSummary = getGroupContextSummary(gId);
        //cout << "***" << groupSummary->getId() << endl;
        auto myContext = getMyContext();
        
        if (myContext != NULL) 
        {
            gd->handleContextSummary(*groupSummary, *myContext);
        }
        performGroupFormations(groupDefinitions, receivedSummaries);
    }
    
    /* 
        Local Summary (MyContext) 
    */
    
    /*
        setMyContext removes the existing summary, and set the new summary to the myContext
    */
    void moveMyContext(ContextSummary& summary)
    {
        // the ownership of summary is moved, if you delete summary, it will cause an error
        this->myContext = unique_ptr<ContextSummary>(&summary);
    }
    void moveMyContext(ContextSummary* summary)
    {
        this->myContext = unique_ptr<ContextSummary>(summary);
    }
    void copyMyContext(ContextSummary& summary)
    {
        //removeLocalSummary();
        this->myContext = unique_ptr<ContextSummary>(new ContextSummary(summary));
    }
    void copyMyContext(ContextSummary* summary)
    {
        //removeLocalSummary();
        this->myContext = unique_ptr<ContextSummary>(new ContextSummary(*summary));
    }
    // This is OK, as we return the reference 
    // of what is already there. 
    ContextSummary* getMyContext()  {return myContext.get();}
    
    void removeLocalSummary()
    {
        if (myContext.get() != NULL)
            myContext.reset();
    }
    
    void updateLocalSummaryByMoving(ContextSummary* summary)
    {
        return updateLocalSummaryByMoving(*summary);
    }    
    
    void updateLocalSummaryByMoving(ContextSummary& summary)
    {
        // from summary, deepcopy the object 
        //removeLocalSummary();
        this->myContext = unique_ptr<ContextSummary>(new ContextSummary(summary));
        
        for (auto& groupDefiniton: groupDefinitions)
        {
            int gId = groupDefiniton.second->getId();
            // getX always returns pointer
            // the input is always reference
            auto groupSummary = getGroupContextSummary(gId);
            groupDefiniton.second->handleContextSummary(*groupSummary, *myContext.get());
        }
    }
    
    void handleIncomingSummaries(const vector<unique_ptr<ContextSummary>>& summaries)
    {
        vector<unique_ptr<ContextSummary>> summariesToPut;
        auto myContext = getMyContext();
        vector<int> receivedSummaryIds = Util::getKeys(receivedSummaries);
        for (auto& summary: summaries)
        {
            int uid = summary->getId();
            summary->incrementHops();
            if (myContext != NULL && myContext->getId() == uid) continue; // skip if the summary is me
            
            if (Util::in(receivedSummaryIds, uid))
            {
                auto existing = getReceivedSummary(uid);
                auto summaryTimeStamp = summary->getTimestamp();
                auto existingTimeStamp = existing->getTimestamp();
                if ( ((summaryTimeStamp < existingTimeStamp) || (summaryTimeStamp == existingTimeStamp)) \
                       && (summary->getHops() >= existing->getHops()))
                       continue;
                // Is this OK? What would be the policy? Copy or reference copy? 
                summariesToPut.push_back(unique_ptr<ContextSummary>(new ContextSummary(*summary)));
            }
        }
        performGroupFormations(this->groupDefinitions, summariesToPut);
    }
    
    // Don't forget that get returns pointer. 
    unique_ptr<ContextSummary> get(int uid)
    {
        if (getMyContext() != NULL && myContext->getId() == uid) {
            return unique_ptr<ContextSummary>(new ContextSummary(*myContext.get()));
        }
        if (Util::in(Util::getKeys(groupContextSummaries), uid)) {
            return unique_ptr<GroupContextSummary>(new GroupContextSummary(*getGroupContextSummary(uid)));
        }
        if (Util::in(Util::getKeys(receivedSummaries), uid)) {
            return unique_ptr<ContextSummary>(new ContextSummary(*getReceivedSummary(uid)));
        }
        return unique_ptr<ContextSummary>(reinterpret_cast<ContextSummary*>(NULL));
    }
    
    vector<ContextSummary*> getSummariesToSend()
    {
        vector<ContextSummary*> result;
        
        if (getMyContext() != NULL) {
            result.push_back(getMyContext()); // unique_ptr<ContextSummary>(new ContextSummary(*getMyContext())));
        }
        
        for (auto& groupSummary: groupContextSummaries)
        {
            GroupContextSummary* summaryPointer = groupSummary.second.get();
            //auto uniquePtr = unique_ptr<GroupContextSummary>(new GroupContextSummary(*summaryPointer));
            result.push_back(summaryPointer); 
        }
        
        for (auto& summary: receivedSummaries)
        {
            int hops = summary.second->getHops();
            if (hops < this->tau)
            {
                ContextSummary* summaryPointer = summary.second.get();
                //auto uniquePtr = unique_ptr<GroupContextSummary>(new GroupContextSummary(*summaryPointer));
                result.push_back(summaryPointer); // unique_ptr<ContextSummary>(new ContextSummary(*summaryPointer)));
            }
        }
        return result;
    }
    
    void setTauAndRemoveSummaries(int tau)
    {
        //TODO
        // How to find the item to remove during iterations?
        setTau(tau);
        vector<int> deleteKeys;
        for (auto& summary: receivedSummaries)
        {
            int hops = summary.second->getHops();
            if (hops >= tau)
            {
                // get the pointer and delete it.
                deleteKeys.push_back(summary.first);
            }
        }
        for (int key: deleteKeys)
        {
            auto ip = receivedSummaries.find(key);
            //auto ip = find(receivedSummaries.begin(), receivedSummaries.end(), key);
            receivedSummaries.erase(ip);
        }
    }
}; 
    
//   ??? Do we need to return copied one? or naive one?               
//     def getGroupSummary(self, gid):
//         groupSummary = self.groupContextSummaries[gid]
//         if groupSummary is not None:
//             return groupSummary.getGroupCopy()
//         return None
#endif