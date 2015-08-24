
#include "murle.h"





////////////////////////////////////////////////////////////////////////
// user
////////////////////////////////////////////////////////////////////////


#define T1 B4
#define T2 A4
#define T3 G4

#define PRINT_NOTE(T) Serial.print(#T);

Wave n1(NOTE_B4);
Wave n2(NOTE_A4);
Wave n3(NOTE_G4);

#define getting_tone_pin 13

void setup() {
  Serial.begin(9600);
  setup_motor();
  setup_microphone();
  //code_for_frequencies();
  Serial.print(n1.frequency()); Serial.print("\t"); Serial.print(n2.frequency()); Serial.print("\t"); Serial.print(n3.frequency()); Serial.println();
  Serial.println("---\t---\t---"); 
  pinMode(getting_tone_pin, OUTPUT);
}

int last_set_frequency;
int last_frequency;
int current_frequency;
int same_counter;

#define min_value 10
#define multiplier 5

#define tone_same_count 2
#define silence_same_count 5

void loop() {
  listen_to_sound(1000);
  Intensity i1 = n1.intensity();
  Intensity i2 = n2.intensity();
  Intensity i3 = n3.intensity();
  Serial.print(i1); Serial.print("\t"); Serial.print(i2); Serial.print("\t"); Serial.print(i3); Serial.print("\t");
  last_frequency = current_frequency;
  current_frequency = 0;
  if (i1 > min_value && i2 > min_value && i3 > min_value) {
    if        (i1 / multiplier > i2 && i1 / multiplier > i3) {
      current_frequency = n1.frequency();
    } else if (i2 / multiplier > i1 && i2 / multiplier > i3) {
      current_frequency = n2.frequency();
    } else if (i3 / multiplier > i1 && i3 / multiplier > i2) {
      current_frequency = n3.frequency();
    }
  }
  if (current_frequency == last_frequency) {
    same_counter++;
    
  } else {
    same_counter = 1;
  }
  boolean switch_action = same_counter >= tone_same_count || last_set_frequency == 0;
  if (current_frequency == n1.frequency()) {
    PRINT_NOTE(T1); 
    if (switch_action) {
      motor(0, 255);
      last_set_frequency = n1.frequency();
    }
  } else if (current_frequency == n2.frequency()) {
    PRINT_NOTE(T2);
    if (switch_action) {
      motor(255, 255);
      last_set_frequency = n2.frequency();
    }
  } else if (current_frequency == n3.frequency()) {
    PRINT_NOTE(T3);
    if (switch_action) {
      motor(255, 0);
      last_set_frequency = n3.frequency();
    }
  } else if (current_frequency == 0){
    
    if (same_counter > silence_same_count) {
      Serial.print("S");
      motor(0,0);
      last_set_frequency = 0;
    }
  }
  // show that we are getting a tone
  if (current_frequency == 0) {
    digitalWrite(getting_tone_pin, LOW);
  } else {
    digitalWrite(getting_tone_pin, HIGH);
  }
  Serial.println(); // last instruction of the loop
}






