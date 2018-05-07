# active-print
Alle ps- und pdf-Dateien, die nach ~/print kopiert werden, werden automatisch
ausgedruckt.
Zuerst muß in ~/print für jeden Drucker ein Verzeichnis angelegt werden.
Meine Drucker heißen laserjet und duplex.
Also muß es die Verzeichnisse ~/print/laserjet und ~/print/duplex geben.
Außerdem muß es in ~/.config/autostart eine Datei active-print-laserjet.desktop
und eine Datei active-print-duplex.desktop geben.
Kopieren Sie dazu active-print.desktop.
Editieren Sie dann die beiden Dateien, um die korrekte Python-Datei aufzurufen. 
Es muß in ~/bin die Dateien active-print-laserjet.py und active-print-duplex.py
geben.
Sie müssen editiert werden.
Ändern Sie printer = "laserjet" entsprechend der beiden Drucker (laserjet und duplex in meinem Falle).
