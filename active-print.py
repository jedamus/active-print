#!/usr/bin/env python2
# coding=utf8

# erzeugt Donnerstag, 08. Juni 2017 19:05 (C) 2017 von Leander Jedamus
# modifiziert Samstag, 16. Januar 2021 08:00 von Leander Jedamus
# modifiziert Donnerstag, 19. November 2020 09:12 von Leander Jedamus
# modifiziert Sonntag, 15. Juli 2018 17:57 von Leander Jedamus
# modifiziert Dienstag, 05. Juni 2018 01:58 von Leander Jedamus
# modifiziert Montag, 04. Juni 2018 23:53 von Leander Jedamus
# modifiziert Samstag, 05. Mai 2018 16:17 von Leander Jedamus
# modifiziert Donnerstag, 22. Juni 2017 17:20 von Leander Jedamus
# modifiziert Freitag, 16. Juni 2017 01:57 von Leander Jedamus
# modifiziert Montag, 12. Juni 2017 18:47 von Leander Jedamus
# modifiziert Samstag, 10. Juni 2017 12:07 von Leander Jedamus
# modifiziert Freitag, 09. Juni 2017 20:49 von Leander Jedamus
# modifiziert Donnerstag, 08. Juni 2017 19:05 von Leander Jedamus

import os
import sys
import re
import gettext
import logging
from argparse import ArgumentParser
import pynotify
import pyinotify

def can_continue(filename):

  def write_pid(filename,pid):
    filedesc = open(filename,"w")
    filedesc.write("{pid:d}".format(pid=pid))
    filedesc.close()

  pid = os.getpid()
  log.debug("{pid:d}".format(pid=pid))
  log.debug("{filename:s}".format(filename=filename))
  if os.access(filename, os.F_OK):
    log.debug("file existiert.")
    filedesc = open(filename,"r")
    # print(filedesc.readline())
    pidstr = filedesc.readline()
    pid = int(pidstr)
    log.debug("{pid:d}".format(pid=pid))
    filedesc.close()
    befehl = "ps -q " + pidstr + " -o comm= > /dev/null"
    log.debug(befehl)
    ret = os.system(befehl)
    log.debug("{ret:d}".format(ret=ret))
    if (ret == 0):
      log.debug("Prozess mit der Nr. {pid:d} läuft noch.".format(pid=pid))
      return False
    else:
      log.debug("Prozess mit der Nr. {pid:d} läuft nicht mehr.".format(pid=pid))
      pid = os.getpid()
      write_pid(filename,pid)
      return True
  else:
    log.debug("file existiert nicht.")
    write_pid(filename,pid)
    return True

home = os.environ["HOME"]
user = os.environ["USER"]
hat_display = "DISPLAY" in os.environ

log_path_and_filename = os.path.join("/tmp",user + "-active-print.log")

dict_suffix_and_path = {
  "pdf":       "",
  "ps":        "",
};

file_handler = logging.FileHandler(log_path_and_filename)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
log = logging.getLogger()
log.addHandler(file_handler)
log.addHandler(stdout_handler)
log.setLevel(logging.INFO)
#log.setLevel(logging.DEBUG)

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("active-print.py",os.path.join(scriptpath, \
                                                       "locale"))
  trans.install(unicode=True)
except IOError:
  log.error("Fehler in gettext")
  def _(s):
    return s

parser = ArgumentParser(description = _("Copy a PS- or PDF-file in a special directory and the file gets printed."))
parser.add_argument("-P", "--printer", dest="printer", default="laserjet", help = _("select printer"))
printer = parser.parse_args().printer
path_to_watch = os.path.join(home,"print",printer)

if can_continue(os.path.join("/tmp",user + "-active-print-" + printer + ".pid")):
  if hat_display:
    if not pynotify.init(_("Active-Print")):
      log.critical(_("Can't initialize pynotify"))
      sys.exit(1);

  dict_compiled_regex_and_path = {}
  for key in dict_suffix_and_path:
    suffix = re.sub("[.]","[.]","." + key)
    path = dict_suffix_and_path[key]
    path = os.path.join(path_to_watch,path)
    regex = os.path.join(path_to_watch,".*" + suffix);
    compiled_key = re.compile(regex, re.UNICODE)
    dict_compiled_regex_and_path.update({ compiled_key: [key, suffix, path] })

  wm = pyinotify.WatchManager();  # Watch Manager
  mask = pyinotify.IN_CLOSE_WRITE # watched events

  class EventHandler(pyinotify.ProcessEvent):
      def process_IN_CLOSE_WRITE(self, event):
        pathname = event.pathname
        for key in dict_compiled_regex_and_path:
          if key.match(pathname):
            new_path = dict_compiled_regex_and_path[key][2]
            suffix_regex = dict_compiled_regex_and_path[key][1]
            suffix = dict_compiled_regex_and_path[key][0]

            log.debug(_("new_path = {new_path:s}").format(new_path=new_path))
            log.debug(_("suffix_regex = {suffix_regex:s}").format(suffix_regex=suffix_regex))
            log.debug(_("suffix = {suffix:s}").format(suffix=suffix))
            filename = re.sub(os.path.join(".*","(.*") + suffix_regex + ")",
              "\g<1>",pathname)
            filename_without_suffix = re.sub("(.*)" + suffix_regex,"\g<1>",
                                             filename)
            log.debug(_("filename = {filename:s}").format(filename=filename))
            log.debug(_("filename_without_suffix = {filename_without_suffix:s}").format(filename_without_suffix=filename_without_suffix))

            try:
              #os.rename(pathname, os.path.join(new_path,new_filename))
              if suffix == "ps":
                log.debug(_("suffix ist ps"))
                new_pathname = "/tmp/{filename:s}".format(filename=filename_without_suffix + ".pdf")
                log.debug(_("new_pathname = {new_pathname:s}").format(new_pathname=new_pathname))
                log.debug(_("pathname = {pathname:s}").format(pathname=pathname))
                os.system("ps2pdf -sPAPERSIZE=a4 {pathname:s} {new_pathname:s}".format(pathname=pathname,new_pathname=new_pathname))
                os.remove(pathname)
                pathname = new_pathname
                
              os.system("lpr -P{printer:s} {pathname:s}".format(printer=printer,pathname=pathname))
              os.remove(pathname)
              message = _("Printed {filename:s} on {printer:s}").format(filename=filename,printer=printer)
              log.info(message)
              if hat_display:
                n = pynotify.Notification(_("Active-Print"), message)
                if not n.show():
                  log.error(_("Failed to send notification"))
                break;
            except OSError:
              log.error(_("Can't print file {filename:s}").format(filename=filename))

  handler = EventHandler()
  notifier = pyinotify.Notifier(wm, handler)
  wdd = wm.add_watch(path_to_watch, mask, rec=False)

  notifier.loop()
else:
  pass
  log.debug("läuft schon.")

# vim:ai sw=2 sts=4 expandtab

