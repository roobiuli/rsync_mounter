#!/usr/bin/python
import os
import sys
from subprocess import Popen, PIPE
import argparse

par = argparse.ArgumentParser("This script  uses rsync to make a clone from NFS sources you give  \n\
ex: script -H <NFS SERVER HOST> -m <Temporary mount point> -c <Directory where to clone content> \n \n")
par.add_argument("-H", help="Source hosname or ip", required=True, dest="H" )
par.add_argument("-c", help=" Clone Directory", required=False, default="/tmp/clone", dest="C" )
par.add_argument("-m", help="Mount Directory", required=False, default="/tmp/tempmount", dest="M" )

args = par.parse_args()




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
    command = "rsync -avh " + source + "/*" + " " + target
    cop = bash(command)


def main(sourceip):
    ip = sourceip
    command = "showmount -e " + ip + " | grep -i reserved"
    source = bash(command)[0].split() # Take source dir

    if bash(command)[2] == 0:
        dirs = [args.C, args.M]
        for direc in dirs:
            create_dir(direc)
        mounter_cmd = "sudo mount -t nfs -o rw,nfsvers=3 " + \
                            ip + ":" + source[0] + " {}".format(dirs[1])
        mounter = bash(mounter_cmd)[2]
        if mounter == 0:
            rsync(dirs[1], dirs[0])
            cmd = "sudo umount" + dirs[1]
            suc = bash(cmd)[2]
            if suc == 0:
                try:
                    os.rmdir(dirs[1])
                except OSError:
                    print "Could not delete {}".format(dirs[1])
    else:
        print "No shared mount point found for this host "

#if __name__ == " __main__":
main(args.H)
