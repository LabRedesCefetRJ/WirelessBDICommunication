// Inclui biblioteca da Radio Head - Amplitude Shift Keying
#include <RH_ASK.h>

// Inclui biblioteca dependente Serial Peripheral Interface
#include <SPI.h>

RH_ASK rf_driver;

void limparBuffer(uint8_t *buff, uint8_t tamanho) {
    memset(buff, 0, tamanho); // Preenche o buffer com zeros
}

void setup() {
  rf_driver.init();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
}

void loop() {
  uint8_t buff[255];
  uint8_t bufflen = sizeof(buff);
  
  limparBuffer(buff, bufflen); // Garante que o buffer esteja limpo
  
  if (rf_driver.recv(buff, &bufflen)) {
    buff[bufflen] = '\0'; // Garante que a string termine corretamente
    
    Serial.print("Mensagem recebida: ");
    Serial.println((char *)buff);

    const char *msg = "Esta é uma resposta";
    rf_driver.send((uint8_t *)msg, strlen(msg));
    digitalWrite(LED_BUILTIN, HIGH);
    rf_driver.waitPacketSent();
    digitalWrite(LED_BUILTIN, LOW);
  }
}
