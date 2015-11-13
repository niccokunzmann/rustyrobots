
#ifndef motor_h
#define motor_h
#include <Arduino.h>

////////////////////////////////////////////////////////////////////////
// motor
////////////////////////////////////////////////////////////////////////

// pins

#define left_motor_pwm_pin 7
#define left_motor_pin_1   5
#define left_motor_pin_2   8

#define right_motor_pwm_pin 3
#define right_motor_pin_1   4
#define right_motor_pin_2   2

void setup_motor();

// drive

/* Steer the motor.
 * -255 <= strength <= 255
 *
 */
void motor(int left_strength, int right_strength);
void right_motor(int strength);
void left_motor(int strength);




#endif
