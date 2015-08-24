
#include "wave.h"


#define Sample int
#define has_samples (number_of_samples)
#define waited_for_completion (average_sample)

void setup_timer2_frequency(){
  // copied from sound_generator.ino
  //http://www.instructables.com/id/Arduino-Timer-Interrupts/

  cli();//stop interrupts

  //set timer2 interrupt at sample_frequency
    TCCR2A = 0;// set entire TCCR2A register to 0
    TCCR2B = 0;// same for TCCR2B
    TCNT2  = 0;//initialize counter value to 0
    // set compare match register for 4khz increments
    OCR2A = 124;// = (16*10**6) / (4000*32) - 1 (must be <256)
    // turn on CTC mode
    TCCR2A |= (1 << WGM21);
    // Set CSxx bits for 32 prescaler
    // http://www.instructables.com/file/FY3SNSNHFD1FIKG
    TCCR2B |= (1 << CS21 | 1 << CS20);   
    // enable timer compare interrupt
    TIMSK2 |= (1 << OCIE2A);  
  
  sei();//allow interrupts
}

unsigned int sample_index;
volatile boolean recording_samples = false;
volatile Sample* samples = NULL;
volatile unsigned int number_of_samples = 0;

ISR(TIMER2_COMPA_vect){//timer2 interrupt at sample_frequency
  if (recording_samples) {
    if (sample_index >= number_of_samples) {
      // stop sampling
      sample_index = 0;
      recording_samples = false;
    } else {
      // sampling
      samples[sample_index] = analogRead(microphone_pin);
      sample_index ++;
    }
  } 
}

Wave::Wave(int frequency) {
  samples_per_wave_cycle = sampling_frequency / frequency;
  // allocate RAM for sinus and cosinus
  sinus_wave =   (int8_t*)malloc(samples_per_wave_cycle * sizeof(int8_t));
  cosinus_wave = (int8_t*)malloc(samples_per_wave_cycle * sizeof(int8_t));
  // create the waves
  if (sinus_wave != NULL && cosinus_wave != NULL) {
    float multiplier = PI * 2 / samples_per_wave_cycle;
    uint32_t sum_sinus = 0;
    uint32_t sum_cosinus = 0;
    for (int i = 0; i < samples_per_wave_cycle; ++i) {
      int8_t value;
      value = sin(i * multiplier) * 127.;
      sum_sinus   += abs(value);
      sinus_wave[i] = value;
      value = cos(i * multiplier) * 127.;
      sum_cosinus += abs(value);
      cosinus_wave[i] = value;
    }
    sinus_normalizer   = sum_sinus / samples_per_wave_cycle;
    cosinus_normalizer = sum_cosinus / samples_per_wave_cycle;
  }
}

Wave::~Wave() {
  free(sinus_wave);
  free(cosinus_wave);
}

int Wave::error_code() {
  // ERROR 1: frequency too high
  // Cannot sample frequencies greater than sampling_frequency/2.
  if (frequency() > sampling_frequency / 2) return 1;
  // ERROR 2: not enough RAM
  // sampling at this frequency takes a lot of RAM
  if (sinus_wave == NULL) return 2;
  if (cosinus_wave == NULL) return 3;
  // everything is ok
  return 0;
}

int Wave::frequency() {
  return sampling_frequency / samples_per_wave_cycle;
}

int overflow_preventing_intensity_shift;
int average_sample;

void printu32(int32_t i) {
  if (i < 0) {
    Serial.print("-");
    i = -i;
  }
  Serial.print((int)(i / 100000000L)); Serial.print(",");
  Serial.print((int)((i / 10000L) % 10000L)); Serial.print(",");
  Serial.print((int)(i % 10000L));
}

Intensity Wave::intensity() {
  wait_for_sound_to_complete();
  if (!has_samples) return 0;
  // step one, convolve the wave
  // read the book http://www.dspguide.com/ch13/2.htm
  int32_t sum_sinus   = 0;
  int32_t sum_cosinus = 0; 
  for (int sample_index = 0;
       sample_index < number_of_samples;
       sample_index++) 
  {
    int wave_index = sample_index % samples_per_wave_cycle;
    int32_t sample = samples[sample_index] - average_sample;
    sum_sinus   += sample * sinus_wave[wave_index];
    sum_cosinus += sample * cosinus_wave[wave_index];
  }
  // normalize the values
  sum_sinus   /=   sinus_normalizer;
  sum_cosinus /= cosinus_normalizer;
  // compute the squared intensity
  // now I need 15 bits
  sum_sinus   >>= overflow_preventing_intensity_shift;
  sum_cosinus >>= overflow_preventing_intensity_shift;

  if (sum_sinus < -134217727 || sum_sinus > 134217727 || sum_cosinus < -134217727 || sum_cosinus > 134217727) {
    Serial.print("!");
  }
  return square(sum_sinus) + square(sum_cosinus);
}

boolean start_listening_to_sound(int milliseconds) {
  if (milliseconds < 0) return false;
  // lock operation
  // wait for interrupt to stop
  while (recording_samples);
  // create new samples
  free((void*)samples);
  number_of_samples = min((uint32_t)milliseconds * (uint32_t)sampling_frequency / 1000, 
                          maximum_number_of_sample_memory_in_bytes / sizeof(Sample));
  samples = (volatile Sample*)malloc(number_of_samples * sizeof(Sample));
  if (samples == NULL) {
    Serial.println(F("ERROR: allocation of samples failed."));
    number_of_samples = 0; // set has_samples
    return false;
  }
  // start interrupt
  recording_samples = true;
  // reset values for waiting
  average_sample = 0;
  return true;
}

void wait_for_sound_to_complete() {
  if (!has_samples || waited_for_completion) return;
  // lock operation
  // wait for interrupt to stop
  while (recording_samples);
  // compute average sample
  uint32_t sum_of_samples = 0;
  int minimum_sample = 1024;
  int maximum_sample = 0;
  for (int sample_index = 0; sample_index < number_of_samples; sample_index++) {
    int sample = samples[sample_index];
    sum_of_samples += sample;
    if (sample < minimum_sample) minimum_sample = sample;
    if (sample > maximum_sample) maximum_sample = sample;
  }
  average_sample = sum_of_samples / number_of_samples; // set waited_for_completion
  int sample_range = maximum_sample - minimum_sample;
  // compute overflow prevention
  // + 7 bits wave   // exclude! will be removed by normalizer
  // +10 bits sample // exclude! will be computed in the following
  // - 1 bit averaging
  // -15 bits maximum 
  overflow_preventing_intensity_shift = -16;
  uint32_t sample_bits = (uint32_t)number_of_samples * (uint32_t)sample_range;
  while (sample_bits) {
    overflow_preventing_intensity_shift++;
    sample_bits >>= 1;
  }
  if (overflow_preventing_intensity_shift < 0) {
    overflow_preventing_intensity_shift = 0;
  }
}

boolean listen_to_sound(int milliseconds) {
  boolean success = start_listening_to_sound(milliseconds);
  wait_for_sound_to_complete();
  return success;
}

boolean is_listening_to_sound() {
  return recording_samples;
}

void setup_microphone() {
  setup_timer2_frequency();
  pinMode(microphone_pin, INPUT);
}

