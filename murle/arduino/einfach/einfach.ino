
#include "murle.h"





////////////////////////////////////////////////////////////////////////
// user
////////////////////////////////////////////////////////////////////////

void setup() {
  Serial.begin(9600);
  setup_motor();
  setup_microphone();
  //code_for_frequencies();
}

Wave a(NOTE_A3);
Wave e(NOTE_E4);

void loop() {
  listen_to_sound(1000);
  Intensity ia = a.intensity();
  Intensity ie = e.intensity();
  Serial.print(ia); Serial.print("\t"); Serial.print(ie); Serial.print("\t");
  if (ia > 10 && ie > 10) {
    if (ia > ie * 7) {
      Serial.print("A");
    } else if (ie > ia * 7) {
      Serial.print("E");
    }
  }
  Serial.println();
}






