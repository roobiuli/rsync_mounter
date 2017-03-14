
from subprocess import Popen, PIPE

def bash(command):
    proc = Popen(command, shell=True, stderr=PIPE, stdout=PIPE)
    while proc.poll() == None:
        pass
    o, e = proc.communicate()
    return o, e, proc.returncode

var1 = bash("ls /tmp/")
print var1[0]
