#include <SoftwareSerial.h>
SoftwareSerial BEE(11,10);  // (rxPin, txPin)

#define IOPort BEE
#define tmp 500

void setup() {
  IOPort.begin(9600);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (IOPort.available()) {
    char c = IOPort.read();
    Serial.println(c);
    if (c == 'A') {
      digitalWrite(LED_BUILTIN, HIGH);
      IOPort.write('B');
    } else if (c == 'a') {
      digitalWrite(LED_BUILTIN, LOW);
      IOPort.write('b');
    }
  }
}