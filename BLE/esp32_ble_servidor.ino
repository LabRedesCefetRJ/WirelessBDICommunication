#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define LED_PIN 2  // pin 25 for Heltec and 2 for ESP32 Dev Module

BLECharacteristic* pCharacteristic;
bool deviceConnected = false;

#define SERVICE_UUID "12345678-1234-1234-1234-1234567890ab"
#define CHARACTERISTIC_UUID "abcd1234-abcd-1234-abcd-1234567890ab"

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
    Serial.println("BLE client connected");
    digitalWrite(LED_PIN, LOW);
  }

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
    Serial.println("BLE client disconnected");
    digitalWrite(LED_PIN, HIGH);
    BLEDevice::startAdvertising();  // Reinicia advertising
  }
};

class MyCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* pCharacteristic) {
    // Acessa o buffer cru diretamente
    const uint8_t* data = pCharacteristic->getData();
    size_t length = pCharacteristic->getLength();
    if (length > 0) {
      Serial.write(data, length);  // Imprime exatamente os dados recebidos
    }
  }
};

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  BLEDevice::init("ESP32_Server");

  BLEServer* pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService* pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY);
  pCharacteristic->setCallbacks(new MyCallbacks());

  pService->start();
  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->start();
  Serial.println("BLE server ready");
}

void loop() {
  if (deviceConnected && Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    const char* data = msg.c_str();
    size_t totalLength = msg.length(); // Não inclui o '\0'
    size_t offset = 0;

    while (offset < totalLength) {
      size_t chunkSize = std::min<size_t>(20, totalLength - offset);
      pCharacteristic->setValue((uint8_t*)(data + offset), chunkSize);
      pCharacteristic->notify();
      offset += chunkSize;

      delay(10); // Pequeno atraso entre os pacotes (BLE é sensível a isso)
    }
  }
}

