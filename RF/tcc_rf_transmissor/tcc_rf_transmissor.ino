// Inclui biblioteca da Radio Head - Amplitude Shift Keying
#include <RH_ASK.h>

// Inclui biblioteca dependente Serial Peripheral Interface
#include <SPI.h>

RH_ASK rf_driver;

void prepararMensagem(uint8_t *buffer, const char *mensagem, uint8_t tamanhoMaximo) {
    memset(buffer, 0, tamanhoMaximo); // Limpa o buffer
    strncpy((char *)buffer, mensagem, tamanhoMaximo - 1); // Copia a mensagem e evita overflow
}


void setup() {
  rf_driver.init();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
}

void loop() {
  uint8_t buff[20];
  uint8_t bufflen = sizeof(buff);

  // Prepara a mensagem para envio
  prepararMensagem(buff, "Esta é uma mensagem", bufflen);

  rf_driver.send(buff, strlen((char *)buff)); // Envio seguro da mensagem
  rf_driver.waitPacketSent();

  if (rf_driver.available()) {
    rf_driver.recv(buff, &bufflen);
    buff[bufflen] = '\0'; // Garante que a string termine corretamente

    Serial.print("Mensagem recebida: ");
    Serial.println((char *)buff);
  }

  delay(250);
  digitalWrite(LED_BUILTIN, HIGH);

  delay(250);
  digitalWrite(LED_BUILTIN, LOW);
}