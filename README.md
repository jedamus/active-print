# active-print

All ps- and pdf-files, which are COPIED to ~/print/<printername>, are
automatically printed.
Alle ps- und pdf-Dateien, die nach ~/print/<druckername> KOPIERT werden,
werden automatisch ausgedruckt.

## Getting started

Perhaps you have to do this first:

```
sudo apt install notify-osd python-notify python-pyinotify
```

First look at ./install.sh and change the line with 'printers="..."' to
contain the name(s) of your printer(s).
Then:

```
sh ./install.sh
```
