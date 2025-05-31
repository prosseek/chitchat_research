# ID;P
# C;Y1;X1;K"Row 1"
# C;Y2;X1;K"Row 2"
# C;Y3;X1;K"Total"
# C;Y1;X2;K11.3
# C;Y2;X2;K22
# C;Y3;X2;K0;ER1C2+R2C2
# E

# 2014-01-30 20:01:07
# mesh10_*.txt True
# 10.0,10.0,0.0,0.0
# 4.66
# 106.5,0.0

import os.path
f_inputs =["/Users/smcho/Desktop/analysis/results/result_10_100_10_40.txt",
"/Users/smcho/Desktop/analysis/results/result_10_100_10_40.txt",
"/Users/smcho/Desktop/analysis/results/result_10_100_10_80.txt",
"/Users/smcho/Desktop/analysis/results/result_200_500_50_50.txt"]

def process(f_input):
    f = open(f_input)
    r = map(lambda e: e.strip(), f.readlines())

    blocks = []
    result = []
    for l in r:
        if len(l) == 0:
            blocks.append(result)
            result = []
        else:
            result.append(l)

    d, f = os.path.split(f_input)
    f_output = os.path.join(d, f.replace("txt","slk"))
    f = open(f_output, "w")

    print f_output
    totalresult = ""

    result = ""
    pre = """
    C;Y1;X1;K"accu total"
    C;Y1;X2;K"accu single"
    C;Y1;X3;K"accu agg"
    C;Y1;X4;K"no of cohorts"
    C;Y1;X5;K"speed"
    C;Y1;X6;K"single size"
    C;Y1;X7;K"aggr size"
    """
    count = 2
    noCount = 1
    for b in blocks:
        common = "C;Y%d;" % count 
        accu = b[2]; accus = accu.split(",")
        result += common + "X1;K" + str(accus[0]) + "\n"
        result += common + "X2;K" + str(accus[1]) + "\n"
        result += common + "X3;K" + str(accus[2]) + "\n"
        result += common + "X4;K" + str(accus[3]) + "\n"
        #print result
        speed = b[3]
        result += common + "X5;K" + str(speed) + "\n"
        size = b[4]; sizes = size.split(",")
        result += common + "X6;K" + str(sizes[0]) + "\n"
        result += common + "X7;K" + str(sizes[1]) + "\n"
    
        totalresult += (result)
        count += 1
    
        if noCount == 10:
            count += 1
            noCount = 1 
        else:
            noCount += 1
    #print totalresult
    f.write("ID;P\n" + pre + totalresult + "E\n")
    f.close()
    
for f in f_inputs:
    process(f)