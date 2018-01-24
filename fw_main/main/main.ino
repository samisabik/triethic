#include <Arduino.h>
#include <SoftwareSerial.h>
#include <SoftReset.h>

#define   WISOL_RX_PIN      6
#define   WISOL_TX_PIN      5
#define   SENSOR_TRIG_PIN   3
#define   SENSOR_ECHO_PIN   4

SoftwareSerial Sigfox =  SoftwareSerial(WISOL_RX_PIN, WISOL_TX_PIN);
int data_s = 0;
bool timeout = false;

void setup() {

  Serial.begin(9600);

  pinMode(WISOL_RX_PIN, INPUT);
  pinMode(WISOL_TX_PIN, OUTPUT);
  pinMode(SENSOR_TRIG_PIN, OUTPUT);
  pinMode(SENSOR_ECHO_PIN, INPUT);

  Sigfox.begin(9600);
  
  delay(2000);
  Serial.println("\n----------------------------------");
  Serial.print("Sensor_ID : ");
  Serial.print(getID());
  delay(500);
  Serial.print("Voltage : ");
  Serial.println(getVolt());
  delay(500);
  Serial.println("----------------------------------");
  delay(500);
  Serial.print("First Message : ");
  data_s = getDistance();
  Serial.print(data_s);
  sendMessage(data_s);
  Serial.print("... succes!");
  Serial.println("----------------------------------");
}

void loop() {
    data_s = getDistance();
    sendMessage(data_s);
    Serial.print("/ payload : ");
    Serial.println(data_s);
    delay(300000);
}

String getID(){
  String id = "";
  char output;
  unsigned long started_at = millis();
  Sigfox.print("AT$I=10\r");
  delay(200);
  while (!Sigfox.available()){
    if (millis() - started_at > 3000 )
        Serial.println("... timeout!");
        delay(200);
  }

  while(Sigfox.available()){
    output = Sigfox.read();
    id += output;
    delay(20);
  }

  return id;
}

String getVolt(){
  String volt = "";
  char output;
  unsigned long started_at = millis();
  int i = 0;
  Sigfox.print("AT$V?\r");
  delay(200);
  while (!Sigfox.available()){
    if (millis() - started_at > 3000 )
        Serial.println("... timeout!");
        delay(200);
  }

  while(Sigfox.available() && i < 4){
    output = Sigfox.read();
    volt += output;
    delay(20);
    i++;
  }

  return volt;
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

