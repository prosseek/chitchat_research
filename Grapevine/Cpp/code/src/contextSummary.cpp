#include <sstream>
#include <cassert>
#include "contextSummary.h"
#include "util.h"

ContextSummary& ContextSummary::operator=(const ContextSummary& other)
{
    this->id = other.id;
    this->hops = other.hops;
    this->timestamp = other.timestamp;
    
    //TODO
    // Now it just copies the pointer of the db, but it may be deepcopy ultimately
    this->db = other.db;
    return *this;
}

std::vector<std::string> ContextSummary::keySet() const
{
    //assert (db != NULL);
    return Util::getKeys((this->db));
}

std::string ContextSummary::to_string() const
{
    std::string dbString = Util::to_string(db);
    
    std::ostringstream out;  
    out << "(" << this->id << ")" << "[" << this->hops << "]:" << dbString << "-(" << this->timestamp << ")"; 
    
    return out.str();
}

bool ContextSummary::sameExceptHops(const ContextSummary& other)
{
    return (this->id == other.id) && \
           (this->db == other.db) && \
           (this->timestamp == other.timestamp);
}

bool ContextSummary::operator==(const ContextSummary& other)
{
    return sameExceptHops(other) && this->hops == other.hops;
}

void ContextSummary::put(const std::string& key, int value)
{
    db[key] = value;
}

bool ContextSummary::containsKey(std::string key) const
{
    auto it = db.find(key);
    if (it == db.end()) return false;
    return true;
}

void ContextSummary::remove(std::string key)
{
    //assert (db != NULL);
    std::map<std::string,int>::iterator it = db.find(key);
    if (it == db.end()) return;
    db.erase(it);
}

/*
 * WARNING
 * The pointer should be freed!!!
 */
ContextSummary* ContextSummary::getWireCopy()
{
    ContextSummary* newCopy = new ContextSummary(*this);
    return newCopy;
}

ContextSummary* ContextSummary::getCopy()
{
    return getWireCopy();
}

int ContextSummary::incrementHops()
{
    int hops = this->getHops();
    return this->setHops(hops+1);
}