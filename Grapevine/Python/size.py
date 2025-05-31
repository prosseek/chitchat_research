#execute(r"find . -name "*.cc" -print | wc")

from subprocess import *
# p = subprocess.Popen(['find', '.', '-name', "*.cc", "-print", "|", "xargs", "wc"], 
#     stdout=subprocess.PIPE, 
#     stderr=subprocess.PIPE,
#     shell=True)
# out, err = p.communicate()
# print out


p1 = Popen(['find', './test', '-name', "*.py", "-print"], stdout=PIPE)
p2 = Popen(["xargs", "wc"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
print "test" + output
res = output.split('\n')[-2]
print res
a1 =  res.split(' ')[4]
a1 = int(a1.strip())


p1 = Popen(['find', './src', '-name', "*.py", "-print"], stdout=PIPE)
p2 = Popen(["xargs", "wc"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
print "src" + output
res = output.split('\n')[-2]
print res
a1 =  res.split(' ')[5]
a1 = int(a1.strip())
