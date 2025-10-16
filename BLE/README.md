# Comunicação via Bluetooth Low Energy (BLE)

Conjunto de códigos Arduíno para realizar a comunicação sem fio em BLE usando ESP32.

## Configurações

Por se tratar de um ESP32, foi necessário instalar a placa no Arduino IDE. Para isso, acesse `File > Preferences` e adicione o seguinte link no campo `Additional Boards Manager URLs`:

```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

Em seguida, vá em `Tools > Board > Board Manager`, busque por `esp32` e instale a placa da Espressif.

Para selecionar a placa, vá em `Tools > Board > esp32` e escolha `ESP32 Dev Module`.

## Pinagem

A conexão do ESP32 com o Arduino é feita via USB (USB-C ou micro USB, a depender do modelo), portanto não há necessidade de pinagem específica para a comunicação BLE. O ESP32 já possui suporte nativo para BLE, e a comunicação pode ser realizada diretamente através de suas bibliotecas. Caso o cabo USB não esteja funcionando corretamente, pode ser que o seu cabo seja apenas de energia e não de dados (se for um cabo de carregador de celular, pode ser que este seja o caso).
