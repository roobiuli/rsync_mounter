#!/usr/bin/python
import os
import sys
from subprocess import Popen, PIPE



def bash(command):
    """
    Bash wrapper to move arround
    """
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    while proc.poll() is None:
        pass

    out, err = proc.communicate()
    return out.strip(), err.strip(), proc.returncode


def create_dir(name):
    """
    Create OS directories where the mountpoint and new location will
    be available
    """
    if os.path.exists(name):
        print "Found dir {} ... atempting to delete".format(name)
        try:
            os.removedirs(name)
        except OSError:
            print "Unable to delete {} Please remove it manualy".format(name)
            sys.exit(1)
    try:
        os.makedirs(name)
        #os.chown(name, root, )
    except OSError:
        print "Could not create directory: {}".format(name)
        sys.exit(1)



def rsync(source, target):
    """
    Make Rsync copy
    """
    command = "rsync -avh " + source + " " + target
    #try:
    cop = bash(command)
    cop[0]
    #except OSError:
     #   print "Can\'t copy"
      #  sys.exit(1)



def main(sourceip):
    ip = sourceip
    command = "showmount -e " + ip + " | grep -i reserved"
    source = bash(command)[0].split() # Take source dir
   
    print source
    if bash(command)[2] == 0:
        print "Found NFS share"
        dirs = ["/tmp/newdest", "/tmp/mount"]
        for direc in dirs:
            create_dir(direc)

        mounter_cmd = "sudo mount -t nfs -o rw,nfsvers=3 " + ip + source[0] + " {}".format(dirs[1])
        print "Passed the mount"
        print mounter_cmd
        mounter = bash(mounter_cmd)[2]
        print mounter
        if mounter == 0:
            print "Should start rsync but no !"
            #rsync(dirs[1], dirs[0])
    else:
        print "Not found"

#if __name__ == " __main__":
main('192.168.1.2')
