#include <SoftwareSerial.h>
SoftwareSerial IOPort(11,10); // RX, TX

void setup() {
  // put your setup code here, to run once:
  IOPort.begin(9600);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    IOPort.print(Serial.readString());
  }
  if (IOPort.available()) {
    Serial.print(IOPort.readString());
  }
}
