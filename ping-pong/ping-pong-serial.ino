#include <SoftwareSerial.h>
SoftwareSerial IOPort(11,10); // RX, TX

void setup() {
  IOPort.begin(9600);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    IOPort.print(Serial.readString());
  }
  if (IOPort.available()) {
    Serial.print(IOPort.readString());
  }
}
