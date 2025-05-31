#ifndef __CONTEXT_SUMMARY_H__
#define __CONTEXT_SUMMARY_H__

#include <string>
#include <map>
#include <ctime>
#include <cstddef>
#include <vector>
#include <iostream>

class ContextSummary {
    int id;
    int hops;
    std::map<std::string, int> db {};
    std::time_t timestamp;
    
public:
    ~ContextSummary()
    {
        // std::cout << "Dying ...\n";
    }
    ContextSummary() : ContextSummary(-1)
    {
    }
    
    ContextSummary(const ContextSummary& other)
    {
        //std::cout << "copy constructor";
        this->id = other.id;
        this->hops = other.hops;
        this->timestamp = other.timestamp;
        this->db = other.db;
    }
    
    ContextSummary(int id) // , const std::map<std::string, int>& db = {}, int hops = 3, std::time_t timestamp = 0)
    {
        this->id = id;
        this->db = {};
        this->hops = 3;
        this->timestamp = 0;
    }

    ContextSummary(int id, const std::map<std::string, int>& db, int hops = 3, std::time_t timestamp = 0)
    {
        this->id = id;
        this->db = db;
        this->hops = hops;
        this->timestamp = timestamp;
    }

    ContextSummary& operator=(const ContextSummary& other);
    
    bool sameExceptHops(const ContextSummary& other);
    bool operator==(const ContextSummary& other);
    
    /**
     *   size() returns the elements in this->db
     */
    int size() const { return db.size();}
    
    /**
     * keySet() returns the vector string that contains all the keys in this->db
     */
    std::vector<std::string> keySet() const;
    
    std::time_t getTimestamp() const {return this->timestamp;}
    void setTimestamp(std::time_t timestamp) {this->timestamp = timestamp;}
    
    int getHops() const {return this->hops;}
    int setHops(int hops) {this->hops = hops; return hops;}
    
    int getId() const {return this->id;}
    void setId(int id) {this->id = id;}
    
    std::map<std::string, int> getDb() const {return this->db;}
    
    /**
     * to_string() returns a string format for ContextSummary object
     * http://stackoverflow.com/questions/16431442/c-struct-passing-const-as-this-argument-discards-qualifiers
     */
    std::string to_string() const;
    
    /**
     * get(key) returns the value from the db
     */
    //bool get(const std::string& key, int& result);
    bool get(const std::string& key, int& result) const
    {
        //assert (db != NULL);
        bool contained = containsKey(key);
        if (contained == true) {
            result = db.at(key); // [key];
            return true;
        }
        return false;
    }
    
    /**
     * put(key, val) sets the db[key] into val
     */
    void put(const std::string& key, int value);
    
    bool containsKey(std::string key) const;
    void remove(std::string key);
    ContextSummary* getWireCopy();
    ContextSummary* getCopy();
    int incrementHops();
};

#endif