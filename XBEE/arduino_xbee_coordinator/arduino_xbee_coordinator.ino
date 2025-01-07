#include <SoftwareSerial.h>
SoftwareSerial BEE(11,10);  // (rxPin, txPin)

#define IOPort BEE
#define tmp 2000

void setup() {
  IOPort.begin(9600);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("Transmissor iniciado");
}

void beepbeep() {
  if (IOPort.available()) {
    char c = IOPort.read();
    Serial.println(c);
    if (c == 'B') {
      digitalWrite(LED_BUILTIN, LOW);
      delay(tmp/5);
      digitalWrite(LED_BUILTIN, HIGH);
      delay(tmp/5);
      digitalWrite(LED_BUILTIN, LOW);
      delay(tmp/5);
      digitalWrite(LED_BUILTIN, HIGH);
      delay(tmp/5);
      digitalWrite(LED_BUILTIN, LOW);
      delay(tmp/5);
    } else if (c == 'b') {
      digitalWrite(LED_BUILTIN, LOW);
      delay(tmp/5);
      digitalWrite(LED_BUILTIN, HIGH);
      delay(tmp/5);
      digitalWrite(LED_BUILTIN, LOW);
      delay(tmp/5);
    }
  }
}

void loop() {
  IOPort.write('A');
  digitalWrite(LED_BUILTIN, HIGH);
  delay(tmp);
  beepbeep();
  digitalWrite(LED_BUILTIN, LOW);
  IOPort.write('a');
  delay(tmp);
  beepbeep();
}
