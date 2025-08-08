#include <RH_ASK.h>
#include <SPI.h>

RH_ASK rf_driver;

const uint8_t PACKET_SIZE = 60;  // Máximo seguro por pacote
String mensagemRecebida = "";    // String dinâmica para receber pacotes

void setup() {
  Serial.begin(9600);
  rf_driver.init();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  verificarSerial();
  verificarRadio();
}

void verificarSerial() {
  if (Serial.available() > 0) {
    String mensagem = Serial.readStringUntil('\n');  // Lê toda a string até Enter
    mensagem += "[FIM]";                             // Adiciona marcador de final

    enviarMensagem(mensagem);
  }
}

void verificarRadio() {
  uint8_t bufflen = PACKET_SIZE + 1;
  char pacote[PACKET_SIZE + 1];

  if (rf_driver.recv((uint8_t *)pacote, &bufflen)) {
    pacote[bufflen] = '\0';            // Garante terminação correta
    String recebido = String(pacote);  // Converte para String

    int indexOfEnd = recebido.indexOf("[FIM]");

    if (indexOfEnd != -1) {
      // Remove "[FIM]" da string antes de exibir
      recebido.remove(indexOfEnd, 5);
      mensagemRecebida += recebido;

      Serial.println(mensagemRecebida);
      mensagemRecebida = "";  // Reseta buffer da string
    } else {
      // Continua reconstrução
      mensagemRecebida += recebido;
    }

    piscarLED();
  }
}


void enviarMensagem(String msg) {
  uint16_t tamanho = msg.length();
  uint16_t inicio = 0;

  if (tamanho > 60) {
    while (inicio < tamanho) {
      String pacote = msg.substring(inicio, inicio + PACKET_SIZE);

      rf_driver.send((uint8_t *)pacote.c_str(), pacote.length());
      rf_driver.waitPacketSent();

      inicio += PACKET_SIZE;
      delay(10);  // Pequeno delay para evitar congestionamento
    }
  } else {
    rf_driver.send((uint8_t *)msg.c_str(), tamanho);
    rf_driver.waitPacketSent();
  }

  piscarLED();
}

void piscarLED() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
}
