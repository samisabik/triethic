#include <Arduino.h>
#define   SENSOR_TRIG_PIN   3
#define   SENSOR_ECHO_PIN   4

int data_s = 0;

void setup() {

  Serial.begin(9600);
  pinMode(SENSOR_TRIG_PIN, OUTPUT);
  pinMode(SENSOR_ECHO_PIN, INPUT);
}

void loop() {
    data_s = getDistance();
    Serial.println(data_s);
    delay(500);
}

int getDistance() {
  long duration, distance;
  digitalWrite(SENSOR_TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(SENSOR_TRIG_PIN, HIGH);
  delayMicroseconds(10); 
  digitalWrite(SENSOR_TRIG_PIN, LOW);
  duration = pulseIn(SENSOR_ECHO_PIN, HIGH);
  distance = (duration/2) / 29.1;
  return distance;
}
