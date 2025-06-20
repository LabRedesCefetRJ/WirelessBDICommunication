#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define LED_PIN 2 // pin 25 for Heltec and 2 for ESP32 Dev Module

unsigned long lastReconnectAttempt = 0;
const unsigned long reconnectInterval = 5000; // 5 segundos

static BLEUUID serviceUUID("12345678-1234-1234-1234-1234567890ab");
static BLEUUID charUUID("abcd1234-abcd-1234-abcd-1234567890ab");

static boolean doConnect = false;
static boolean connected = false;
static BLERemoteCharacteristic* pRemoteCharacteristic;
static BLEAdvertisedDevice* myDevice;

class MyClientCallback : public BLEClientCallbacks {
    void onConnect(BLEClient* pclient) {
      connected = true;
      digitalWrite(LED_PIN, LOW);
      Serial.println("Connected to BLE Server.");
    }

    void onDisconnect(BLEClient* pclient) {
      connected = false;
      Serial.println("Disconnected");
      digitalWrite(LED_PIN, HIGH);

      // Libera dispositivo antigo
      doConnect = false;
      if (myDevice) {
        delete myDevice;
        myDevice = nullptr;
      }

      // Aguarda para nova tentativa
      lastReconnectAttempt = millis();
    }
};

String buffer = "";
int expectedLength = -1;
bool collecting = false;

static void notifyCallback(BLERemoteCharacteristic* pBLERemoteCharacteristic,
                          uint8_t* pData, size_t length, bool isNotify) {
  for (size_t i = 0; i < length; i++) {
    Serial.print((char)pData[i]);
  }

  // Adiciona conteúdo ao buffer
  for (size_t i = 0; i < length; i++) {
    buffer += (char)pData[i];
  }

  // Se ainda não temos o tamanho esperado, tentamos extrair
  if (!collecting && buffer.startsWith("fffe") && buffer.length() >= 6) {
    String hexLength = buffer.substring(4, 6); // Dois caracteres hexadecimais
    expectedLength = strtol(hexLength.c_str(), nullptr, 16);
    expectedLength += 6; // soma o tamanho do cabeçalho também
    collecting = true;
  }

  // Se já temos o tamanho esperado e recebemos tudo
  if (collecting && buffer.length() >= expectedLength) {

    // Limpa para próxima mensagem
    buffer = buffer.substring(expectedLength);
    expectedLength = -1;
    collecting = false;
  }
}


bool connectToServer() {
    Serial.print("Connecting to ");
    Serial.println(myDevice->getAddress().toString().c_str());

    BLEClient* pClient = BLEDevice::createClient();
    pClient->setClientCallbacks(new MyClientCallback());
    pClient->connect(myDevice);

    BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
    if (pRemoteService == nullptr) {
      Serial.println("Failed to find service");
      pClient->disconnect();
      return false;
    }

    pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);
    if (pRemoteCharacteristic == nullptr) {
      Serial.println("Failed to find characteristic");
      pClient->disconnect();
      return false;
    }

    if (pRemoteCharacteristic->canNotify()) {
      pRemoteCharacteristic->registerForNotify(notifyCallback);
    }

    return true;
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(serviceUUID)) {
        BLEDevice::getScan()->stop();
        myDevice = new BLEAdvertisedDevice(advertisedDevice);
        doConnect = true;
      }
    }
};

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  BLEDevice::init("");
  BLEScan* pScan = BLEDevice::getScan();
  pScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pScan->setActiveScan(true);
  pScan->start(5);
}

void loop() {
  if (doConnect) {
    if (connectToServer()) {
      Serial.println("Connected to BLE Server.");
    } else {
      Serial.println("Failed to connect.");
      lastReconnectAttempt = millis();  // Marca para tentar mais tarde
    }
    doConnect = false;
  }

  if (connected && Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    pRemoteCharacteristic->writeValue(msg.c_str(), msg.length() + 1);
  }

  // Se desconectado, tenta reconectar após intervalo
  if (!connected && !doConnect) {
    if (millis() - lastReconnectAttempt > reconnectInterval) {
      Serial.println("Trying to reconnect...");
      BLEScan* pScan = BLEDevice::getScan();
      pScan->start(5, false);  // Não bloquear
      lastReconnectAttempt = millis();
    }
  }
}
