#execute(r"find . -name "*.cc" -print | wc")

from subprocess import *
# p = subprocess.Popen(['find', '.', '-name', "*.cc", "-print", "|", "xargs", "wc"], 
#     stdout=subprocess.PIPE, 
#     stderr=subprocess.PIPE,
#     shell=True)
# out, err = p.communicate()
# print out


p1 = Popen(['find', '.', '-name', "*.cc", "-print"], stdout=PIPE)
p2 = Popen(["xargs", "wc"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
res = output.split('\n')[-2]
print "test  :" + res
a1 =  res.split(' ')[4]
a1 = int(a1.strip())

p1 = Popen(['find', '.', '-name', "*.h", "-print"], stdout=PIPE)
p2 = Popen(["xargs", "wc"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
res = output.split('\n')[-2]
print "header:" + res
a2 =  res.split(' ')[4]
a2 = int(a2.strip())

p1 = Popen(['find', '.', '-name', "*.cpp", "-print"], stdout=PIPE)
p2 = Popen(["xargs", "wc"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
res = output.split('\n')[-2]
print "code  :" + res
a3 =  res.split(' ')[5]
#print a3
a3 = int(a3.strip())

print (a1 + a2 + a3)