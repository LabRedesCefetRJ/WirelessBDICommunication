# Comunicação via Radiofrequência 

Conjunto de códigos Arduíno para realizar a comunicação sem fio usando módulos de Radiofrequência.

## Configurações

Os módulos não preecisam de comunicação, entretanto é necessário implementar uma camada de protocolo para garantir a integridade dos dados. No caso, foi implementada a biblioteca `Radio Head - Amplitude Shift Keying` para realizar a comunicação.

Mais informações na [Documentação da biblioteca](https://www.airspayce.com/mikem/arduino/RadioHead/classRH__ASK.html).

## Pinagem

Existe um módulo RF para transmissão e outro para recepção. Não é necessário configurar os módulos, basta conectá-los ao Arduíno A biblioteca tem como padrão a transmissão pela porta `12` e a recepção pela porta `11`.

|  RX  | Arduino |
|------|---------|
|  5V  |  5V     |
|  GND |  GND    |
|  RX  |  11 (RX)|

|  TX  | Arduino |
|------|---------|
|  5V  |  5V     |
|  GND |  GND    |
|  TX  |  12 (TX)|

Adicionalmente, foram conectadas antenas de 34,56 cm (1/2 do cumprimento de onda) para aumentar o alcance do sinal na porta de antena para cada módulo.

Note que as portas `RX` e `TX` devem ser conectadas às portas `TX` e `RX` do Arduino, respectivamente, para os dois módulos.
