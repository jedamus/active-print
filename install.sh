#!/usr/bin/env sh

# erzeugt Montag, 14. Dezember 2020 14:23 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 15. Dezember 2020 09:05 von Leander Jedamus
# modifiziert Montag, 14. Dezember 2020 14:23 von Leander Jedamus

# modify this to reflect your printers!
printers="laserjet duplex"

autostart=$HOME/.config/autostart
my_print=$HOME/print
zlogin=$HOME/.zlogin

modify_desktop_file()
{
  echo "installing $2"
  cat $1 | sed "s/USER/$USER/g" | sed "s/PRINTER/$3/g" > $2
};# modify_desktop_file

mkdir -p $autostart

cp -Rvp active-print.py locale $HOME/bin
echo ""

echo "#echo \"ich bin $zlogin\"\n" > $zlogin

# für jeden Druckereintrag ein Verzeichnis anlegen und in .zlogin eintragen:
for i in $printers; do
  echo "creating dir for printer $i"
  mkdir -p $my_print/$i
  echo "echo -n \"active-print.py -P $i: \"" >> $zlogin
  echo "~/bin/active-print.py -P $i 2> /dev/null &" >> $zlogin
done

if [ -d $my_print ]; then
  echo "All PDF files, which are COPIED into these subdrectories of ~/print,\nare printed on the corresponding printer and then DELETED!\n\nAlle PDF-Dateien, die in Unterverzeichnisse von ~/print/ KOPIERT werden,\nwerden auf dem ensprechenden Drucker ausgedruckt und anschließend GELÖSCHT!" > $my_print/README.IMPORTANT\!
fi

for i in $printers; do
  modify_desktop_file active-print.desktop $autostart/active-print-$i.desktop $i
done

# vim:ai sw=2

