Rödel via App Steuern
=====================

[Video](https://www.youtube.com/watch?v=wF0yfeDUJzY&feature=youtu.be)

[![roboterapp.apk](roboterapp.apk.qrcode.png)](https://github.com/niccokunzmann/rustyrobots/raw/master/roedel/raspberrypi/roboterapp.apk)  
Mit diesem QR-Code kann man die [App herunterladen](https://github.com/niccokunzmann/rustyrobots/raw/master/roedel/raspberrypi/roboterapp.apk).

Funktionsweise
--------------

Die App sendet die Servoposition an den Webserver, der auf dem Raspberry PI läuft. Dieser setzt die Position des Servos. Wie steht in [diesen Artikel](http://www.doctormonk.com/2012/07/raspberry-pi-gpio-driving-servo.html). Der Pin 23 wird genutzt. Wo man die Pins findet, steht [hier](http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/). Der Servo hat eine extra batterie und die beiden Grounds (Masse oder Minus -) des RaspberryPi und der Batterie müssen verbunden werden. Nicht die beiden positiven Spannungen verbinden! Dadurch kann der Servo von Pin 23 angepulst werden.


Installation
------------

Der Webserver braucht das Modul `bottle`. 
Das kann man mit `pip-3.2 install bottle` installieren.   Das `RPI.GPIO`-Modul wird auch benutzt. Installation kann man [hier](http://sourceforge.net/p/raspberry-gpio-python/wiki/install/) finden. Meistens ist es schon da.

