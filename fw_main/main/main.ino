#include <Arduino.h>
#include <SoftwareSerial.h>
#include <SoftReset.h>

#define   WISOL_RX_PIN      6
#define   WISOL_TX_PIN      5
#define   SENSOR_TRIG_PIN   9
#define   SENSOR_ECHO_PIN   8

SoftwareSerial Sigfox =  SoftwareSerial(WISOL_RX_PIN, WISOL_TX_PIN);
int data_s = 21;

void setup() {

  Serial.begin(9600);

  pinMode(WISOL_RX_PIN, INPUT);
  pinMode(WISOL_TX_PIN, OUTPUT);
  //pinMode(SENSOR_TRIG_PIN, OUTPUT);
  //pinMode(SENSOR_ECHO_PIN, INPUT);

  Sigfox.begin(9600);
  delay(2000);  
  //debug
  sendMessage(data_s);
  Serial.println("... done!");
  
}

void loop() {
    //unsigned long startMillis = millis();
    //data_s = getDistance();
    //sendMessage(data_s);
    //while (millis() - startMillis < 300000);
}

void sendMessage(int msg){
  Sigfox.print("AT$SF=");
  Sigfox.print(msg,HEX);
  Sigfox.print("\r");
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

