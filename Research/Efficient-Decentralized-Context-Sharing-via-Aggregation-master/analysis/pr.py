import re

def avg(l):
    def _avg(l): return sum(l)*1.0/len(l)
    if len(l) == 0: raise Exception("No member given")
    val = l[0]
    if type(val) is tuple:
        e = zip(*l)
        result = []
        for i in e:
            result.append(_avg(i))
        return result
    else:
        return _avg(l)

f = open("./results.txt", "r")
r = map(lambda i: i.rstrip(),f.readlines())

res = {}
for i, c in enumerate(r):
    if i % 2 == 0:
        key = c
    else:
        res[key] = c
        
#print res
#print len(res)

def comp(i):
    # find the last name
    #print i
    result = re.search("_(\d+)\.txt$", i)
    return int(result.group(1))

s = sorted(res, key=lambda i: comp(i))

speeds = []
packetCounts = []
accuracies = []
for v in res.values():
    #print v
    r = eval(v)
    speed = r['speed']
    packetCount = r['packetCount']
    accuracy = r['accuracy']
    
    speeds.append(speed)
    packetCounts.append(packetCount)
    accuracies.append(accuracy)
    
print avg(speeds)
#print accuracies
print avg(packetCounts)
print avg(accuracies)

    
# 4 values are missing
# 1, 10, 13, 21

# r = filter(lambda i: i.endswith(".txt"), r)
# r = sorted(r)
# print r
# 
# # find duplicate
# prev = r[0]
# result = []
# for i in r[1:]:
#     if i == prev:
#         print("DUP %s" % i)
#     else:
#         result.append(prev)
#         prev = i
# print result
# print len(result)
        
 