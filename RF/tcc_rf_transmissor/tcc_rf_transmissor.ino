// Inclui biblioteca da Radio Head - Amplitude Shift Keying
#include <RH_ASK.h>

// Inclui biblioteca dependente Serial Peripheral Interface
#include <SPI.h>

RH_ASK rf_driver;

void setup() {
  rf_driver.init();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
}

void loop() {
  uint8_t buff[20];
  uint8_t bufflen = sizeof(buff);

  const char *msg = "Esta é uma mensagem";
  rf_driver.send((uint8_t *)msg, strlen(msg));
  rf_driver.waitPacketSent();

  if (rf_driver.available()) {
    rf_driver.recv(buff, &bufflen);
    Serial.print("Mensagem recebida: ");
    Serial.println((char *)buff);
  }

  delay(250);
  digitalWrite(LED_BUILTIN, HIGH);

  delay(250);
  digitalWrite(LED_BUILTIN, LOW);
}
