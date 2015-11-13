
#include "motor.h"

#define motor_pin_1 right_motor_pin_1
#define motor_pin_2 right_motor_pin_2
#define motor_pwm_pin right_motor_pwm_pin

void right_motor(int strength) {
  if (strength < 0) {
    digitalWrite(motor_pin_1, LOW);
    digitalWrite(motor_pin_2, HIGH);
    analogWrite(motor_pwm_pin, -strength);
  } else if (strength == 0) {
    // fast stop
    digitalWrite(motor_pin_1, LOW);
    digitalWrite(motor_pin_2, LOW);
    digitalWrite(motor_pwm_pin, HIGH);
  } else {
    digitalWrite(motor_pin_1, HIGH);
    digitalWrite(motor_pin_2, LOW);
    analogWrite(motor_pwm_pin, strength);
  }
}

#undef motor_pin_1
#undef motor_pin_2
#undef motor_pwm_pin

#define motor_pin_1 left_motor_pin_1
#define motor_pin_2 left_motor_pin_2
#define motor_pwm_pin left_motor_pwm_pin

void left_motor(int strength) {
  if (strength < 0) {
    digitalWrite(motor_pin_1, LOW);
    digitalWrite(motor_pin_2, HIGH);
    analogWrite(motor_pwm_pin, -strength);
  } else if (strength == 0) {
    // fast stop
    digitalWrite(motor_pin_1, LOW);
    digitalWrite(motor_pin_2, LOW);
    digitalWrite(motor_pwm_pin, HIGH);
  } else {
    digitalWrite(motor_pin_1, HIGH);
    digitalWrite(motor_pin_2, LOW);
    analogWrite(motor_pwm_pin, strength);
  }
}

#undef motor_pin_1
#undef motor_pin_2
#undef motor_pwm_pin

void motor(int left_strength, int right_strength) {
  left_motor(left_strength);
  right_motor(right_strength);
}


void setup_motor() {
  pinMode(left_motor_pwm_pin, OUTPUT);
  pinMode(left_motor_pin_1,   OUTPUT);
  pinMode(left_motor_pin_2,   OUTPUT);
  
  pinMode(right_motor_pwm_pin, OUTPUT);
  pinMode(right_motor_pin_1,   OUTPUT);
  pinMode(right_motor_pin_2,   OUTPUT);
  
  motor(0,0);
}
