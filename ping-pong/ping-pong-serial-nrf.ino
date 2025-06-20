#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Definir pinos CE e CSN
#define CE_PIN 9
#define CSN_PIN 10

// Criar objeto RF24
RF24 radio(CE_PIN, CSN_PIN);

// Endereços para comunicação (devem ser iguais nos dois dispositivos, mas invertidos)
const byte addresses[][6] = {"00001", "00002"};

// Definir número do rádio (0 ou 1)
bool radioNumber = 0; // Índice do addresses do rádio (0 para o primeiro dispositivo, 1 para o segundo)

const int MAX_PAYLOAD_SIZE = 32;

void sendLargeMessage(const char* message) {
  size_t totalLength = strlen(message);
  size_t bytesSent = 0;

  while (bytesSent < totalLength) {
    char packet[MAX_PAYLOAD_SIZE];
    size_t bytesRemaining = totalLength - bytesSent;
    size_t chunkSize = min(bytesRemaining, MAX_PAYLOAD_SIZE - 1); // Reservando 1 byte para flag de controle

    // Primeiro byte = 1 se tem mais pacotes depois, 0 se for o último
    packet[0] = (bytesSent + chunkSize < totalLength) ? 1 : 0;
    memcpy(&packet[1], &message[bytesSent], chunkSize);

    radio.stopListening();
    bool success = radio.write(&packet, chunkSize + 1);
    radio.startListening();

    if (success) {
      bytesSent += chunkSize;
    }

    delay(10); // Pequena pausa entre pacotes
  }
}

void setup() {
  Serial.begin(9600);
  radio.begin(); // Inicializar o módulo nRF24L01
  
  radio.setPALevel(RF24_PA_MIN); // Potência de transmissão baixa
  
  if (radioNumber == 0) {
    radio.openWritingPipe(addresses[0]); // Envia para "00002"
    radio.openReadingPipe(1, addresses[0]); // Recebe de "00001"
  } else {
    radio.openWritingPipe(addresses[0]); // Envia para "00001"
    radio.openReadingPipe(1, addresses[0]); // Recebe de "00002"
  }

  radio.startListening(); // Iniciar como receptor
}

void loop() {
  // --- Recepção ---
  static String receivedMessage = "";

  while (radio.available()) {
    char packet[MAX_PAYLOAD_SIZE];
    radio.read(&packet, sizeof(packet));

    bool hasMore = packet[0]; // Flag de controle
    for (int i = 1; i < MAX_PAYLOAD_SIZE; i++) {
      if (packet[i] != '\0') {
        receivedMessage += (char)packet[i];
      }
    }

    if (!hasMore) {
      Serial.print(receivedMessage);
      receivedMessage = "";
    }
  }

  // --- Verifica entrada do usuário via Serial ---
  if (Serial.available() > 0) {
    String userInput = Serial.readStringUntil('\n'); // Lê até Enter
    userInput.trim(); // Remove espaços em branco

    if (userInput.length() > 0) {
      char textToSend[300] = "";
      userInput.toCharArray(textToSend, sizeof(textToSend));
      sendLargeMessage(textToSend);
    }
  }
}