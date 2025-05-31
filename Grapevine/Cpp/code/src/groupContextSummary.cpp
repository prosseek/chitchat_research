#include <sstream>

#include "groupContextSummary.h"
#include "util.h"

void GroupContextSummary::addMemberIds(const std::vector<int>& ids)
{
    for (auto uid : ids)
        addMemberId(uid);
}