#ifndef wave_h
#define wave_h
#include <Arduino.h>

////////////////////////////////////////////////////////////////////////
// microphone
////////////////////////////////////////////////////////////////////////

// type definitions
#define Intensity uint32_t

#define microphone_pin A7
// if you change sampling_frequency, you also need to change setup_timer2_frequency and the code for the frequency
#define sampling_frequency 4000
#define maximum_number_of_sample_memory_in_bytes 1000

// call this before using the microphone
void setup_microphone();

// call this to listen to sound
// this must be caled before waves yield any useful intensity.
// returns whether listening to sound is possible
// if it would take too much memory it returns false otherwise true
// you can adjust maximum_number_of_sample_memory_in_bytes or milliseconds if it returns false
boolean listen_to_sound(int milliseconds);
// call this to start listening and do something else
boolean start_listening_to_sound(int milliseconds);
// wait for sound to complete
void wait_for_sound_to_complete();
// call this if you want to know if the microphone is in use
boolean is_listening_to_sound();

// we use timer 2 to record microphone values
ISR(TIMER2_COMPA_vect);

class Wave {
  private:
    int8_t* sinus_wave;
    int8_t* cosinus_wave;
    unsigned int samples_per_wave_cycle;
    // for normalization
    int sinus_normalizer;
    int cosinus_normalizer;
  public:
  
    Wave(int frequency);
    ~Wave();
    
    // ERROR 0: everything is ok
    // ERROR 1: frequency too high
    // Cannot sample frequencies greater than sampling_frequency/2.
    // ERROR 2: not enough RAM
    // sampling at this frequency takes a lot of RAM
    int error_code();
    
    // the actual frequency the wave listens to
    int frequency();
  
    Intensity intensity();
};


#endif
