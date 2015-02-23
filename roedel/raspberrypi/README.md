Rödel mit Blockly Programmieren
===============================

Es gibt ein [Video](https://www.youtube.com/watch?v=NBPCZgiwuP4&feature=youtu.be), wie der Rödel Roboter mit Blockly programmiert wird.
Auf der Webseite [rustyrobots.pythonanywhere.com](http://rustyrobots.pythonanywhere.com) werden die erreichbaren Roboter gelistet. 
Sourcecode wird an den Roboter geschickt oder im Browser ausgeführt, dank [Blockly](https://developers.google.com/blockly/).


Rödel via App Steuern
=====================

[Video](https://www.youtube.com/watch?v=wF0yfeDUJzY&feature=youtu.be)

[![roboterapp.apk](client/roboterapp.apk.qrcode.png)](https://github.com/niccokunzmann/rustyrobots/raw/master/roedel/raspberrypi/client/roboterapp.apk)  
Mit diesem QR-Code kann man die [App herunterladen](https://github.com/niccokunzmann/rustyrobots/raw/master/roedel/raspberrypi/roboterapp.apk).

Funktionsweise
--------------

Die App sendet die Servoposition an den Webserver, der auf dem Raspberry PI läuft. Dieser setzt die Position des Servos. [RPIO](http://pythonhosted.org/RPIO/pwm_py.html) wird genutzt zur Steurung des Servos. Der GPIO-Pin 11 wird genutzt. Wo man die Pins findet, steht [hier](http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/). Der Servo hat eine extra Batterie und die beiden Grounds (Masse oder Minus -) des RaspberryPi und der Batterie müssen verbunden werden. Nicht die beiden positiven Spannungen verbinden! Dadurch kann der Servo von Pin 23 angepulst werden.

Installation
============

Die Datei [`download_and_install.sh`](robot/download_and_install.sh) kann auf dem Raspberry Pi ausgeführt werden. Wenn dieser Internetzugriff hat, wird der Webserver automatisch installiert.

Alte Verweise
-------------

Wie man selbst den Servo ansteuert, steht in [diesen Artikel](http://www.doctormonk.com/2012/07/raspberry-pi-gpio-driving-servo.html).
