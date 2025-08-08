#include <SoftwareSerial.h>
SoftwareSerial TOOTH(11,10);  // (rxPin, txPin)

#define IOPort TOOTH

void setup() {
  Serial.begin(9600);
  TOOTH.begin(38400);  //AT Command data transmission rate;
}

void loop() {
  if (TOOTH.available()) {
    char x = TOOTH.read();
    Serial.print(x);
  }

  if (Serial.available()) {
    char c = Serial.read();
    TOOTH.print(c);
  }
}