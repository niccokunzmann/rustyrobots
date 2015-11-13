
#include "murle.h"

void setup() {
  setup_motor();
  Serial.begin(9600);
}


void loop() {
  Serial.println("^ FORWARD ^");
  motor(255, 255);
  delay(1000);
  Serial.println("_ BACK _");
  motor(-255, -255);
  delay(1000);
  Serial.println("RIGHT --");
  motor(0, 255);
  delay(1000);
  Serial.println("-- LEFT");
  motor(255, 0);
  delay(1000);
}






