#include <Servo.h> 

/* Einstellungen */

// Steuersteckplaetze fuer den Motor
const int motor_pin_1 = 9;
const int motor_pin_2 = 10;

const int lenkungs_pin = 8;

const int ausrollverzoegerung_in_millisekuden = 300;

/* Deklarationen fuer die Motorsteuerung */

typedef int Richtung;
#define STOP 0
#define NICHT 0
#define VORWAERTS 1
#define RUECKWAERTS -1

Richtung richtung = STOP;
Richtung richtung_vor_dem_stoppen = STOP;

/* Deklarationen fuer die Lenkung */

Servo lenkung;

/* Funktionen fuer die Lenkung */

void lenke_gerade_aus() {
  lenkung.write(90);
  stoppe();
  fahre_weiter();
}

void lenke_links() {
  lenkung.write(0);
  stoppe();
  fahre_weiter();
}

void lenke_rechts() {
  lenkung.write(179);
  stoppe();
  fahre_weiter();
}

void starte_lenkung() {
  lenkung.attach(lenkungs_pin);
}

/* Funktionen fuer das Fahren */

/* richtung ist 
   STOP oder
   VORWAERTS oder 
   RUECKWAERTS
 */
 

void stoppe() {
  if (richtung == STOP) return;
  richtung_vor_dem_stoppen = richtung;
  richtung = STOP;
  digitalWrite(motor_pin_1, LOW);
  digitalWrite(motor_pin_2, LOW);
  delay(ausrollverzoegerung_in_millisekuden);
}

void fahre_vorwaerts() {
  if (richtung == VORWAERTS) return;
  stoppe();
  richtung = VORWAERTS;
  digitalWrite(motor_pin_1, HIGH);
  digitalWrite(motor_pin_2, LOW);
}

void fahre_rueckwaerts() {
  if (richtung == RUECKWAERTS) return;
  stoppe();
  richtung = RUECKWAERTS;
  digitalWrite(motor_pin_1, LOW);
  digitalWrite(motor_pin_2, HIGH);
}

void fahre(int in_richtung) {
  if (in_richtung == VORWAERTS) fahre_vorwaerts();
  if (in_richtung == RUECKWAERTS) fahre_rueckwaerts();
  if (in_richtung == STOP) stoppe();
  return;
}

void fahre_weiter() {
  if (richtung != STOP) return;
  //fahre(richtung_vor_dem_stoppen);
}

void starte_motor() {
  pinMode(motor_pin_1, OUTPUT);
  pinMode(motor_pin_2, OUTPUT);
  lenke_gerade_aus();
  stoppe();
}

/* Programmstart */

void setup() {
  starte_motor();
  starte_lenkung();
}


/* Das Programm 

  folgende Befehle koennen zum Fahren genutzt werden:
  
    fahre_vorwaerts();
    fahre_rueckwaerts();
    stoppe();
    fahre_weiter();
    
  folgende Befehle koennen zum Lenken genutzt werden:
  
    lenke_gerade_aus();
    lenke_links();
    lenke_rechts();
    
*/

void loop() {
  lenke_rechts();
  fahre_rueckwaerts();
  delay(1000);
  lenke_links();
  fahre_vorwaerts();
  delay(1000);
}
