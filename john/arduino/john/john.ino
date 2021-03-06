

int pin_pwm_1 = 9;
int pin_pwm_2 = 10;

void setup() {
  pinMode(pin_pwm_1, OUTPUT);
  pinMode(pin_pwm_2, OUTPUT);
}

void anhalten() {
  analogWrite(pin_pwm_1, 0);
  analogWrite(pin_pwm_2, 0);
  delay(300);
}

void fahre_vor() {
  anhalten();
  analogWrite(pin_pwm_1, 0);
  analogWrite(pin_pwm_2, 500); // 0 <= geschwindigkeit < 1024
}

void fahre_zurueck() {
  anhalten();
  analogWrite(pin_pwm_1, 500); // 0 <= geschwindigkeit < 1024
  analogWrite(pin_pwm_2, 0);
}

void loop () {
  fahre_vor();
  delay(1000);
  fahre_zurueck();
  delay(1000);
}
