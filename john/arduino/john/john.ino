

int pin_enable = 2;
int pin_pwm_1 = 11;
int pin_pwm_2 = 10;

void setup() {
  pinMode(pin_enable, OUTPUT);
  pinMode(pin_pwm_1, OUTPUT);
  pinMode(pin_pwm_2, OUTPUT);
  
  digitalWrite(pin_enable, HIGH); // anschalten
  
}

void loop () {
  digitalWrite(pin_pwm_1, LOW);
  delay(500);
  analogWrite(pin_pwm_2, 180);
  delay(1500); // fahren
  digitalWrite(pin_pwm_2, LOW);
  delay(500);
  analogWrite(pin_pwm_1, 180);
  delay(1500); // fahren
  
}
