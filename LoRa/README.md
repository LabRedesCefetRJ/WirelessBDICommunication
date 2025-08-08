# Comunicação via LoRa

Conjunto de códigos Arduíno para realizar a comunicação sem fio usando módulos LoRa E32-433T20D.

## Configurações

Não foram necessárias configurações adicionais para os módulos LoRa além da conexão física.

## Pinagem

O módulo possui os pinos `VCC`, `GND`, `AUX`, `RXD`, `TXD`, `M0` e `M1`. Para a comunicação serial, foram utilizados os pinos `RX` e `TX` conectados ao Arduino. A pinagem utilizada foi:

| LoRa | Arduino |
|------|---------|
| VCC  | 5V      |
| GND  | GND     |
| RXD  | 51 (TX) |
| TXD  | 50 (RX) |
| AUX  | --      |
| M0   | GND     |
| M1   | GND     |

Por ter sido utilizado um Arduino Mega, foi possível utilizar os pinos 50 e 51 para a comunicação serial com os módulos LoRa, mas as portas `RX` e `TX` podem ser alteradas para outras portas digitais, se necessário, como os pinos 10 e 11. Note que a conexão RX/TX é cruzada, ou seja, a porta `RX` do módulo deve ser conectada à porta `TX` do Arduino e vice-versa.