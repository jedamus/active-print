#!/usr/bin/env python
# coding=utf-8

# erzeugt Sonntag, 15. Juli 2018 15:25 (C) 2018 von Leander Jedamus
# modifiziert Sonntag, 15. Juli 2018 16:40 von Leander Jedamus

from __future__ import print_function
import os

user = os.environ["USER"]
filename = os.path.join("/tmp",user + "-demonize.pid")
pid = os.getpid()

def write_pid(filename,pid):
  filedesc = open(filename,"w")
  filedesc.write("{pid:d}".format(pid=pid))
  filedesc.close()

print("{pid:d}".format(pid=pid))
print("{filename:s}".format(filename=filename))
if os.access(filename, os.F_OK):
  print("file existiert.")
  filedesc = open(filename,"r")
  # print(filedesc.readline())
  pidstr = filedesc.readline()
  pid = int(pidstr)
  print("{pid:d}".format(pid=pid))
  filedesc.close()
  befehl = "ps -q " + pidstr + " -o comm= > /dev/null"
  print(befehl)
  ret = os.system(befehl)
  print("{ret:d}".format(ret=ret))
  if (ret == 0):
    print("Prozess mit der Nr. {pid:d} läuft noch.".format(pid=pid))
  else:
    print("Prozess mit der Nr. {pid:d} läuft nicht mehr.".format(pid=pid))
    pid = os.getpid()
    write_pid(filename,pid)
else:
  print("file existiert nicht.")
  pid = 3722
  write_pid(filename,pid)

# vim:ai sw=2 sts=4 expandtab

