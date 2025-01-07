# Comunicação via XBEE

Conjunto de códigos Arduíno para realizar a comunicação sem fio usando módulos XBEE.

## Configurações

Para configurar os módulos XBEE, é necessário utilizar o software XCTU. Os módulos devem ser configurados para operar em modo API, com o mesmo PAN ID e com os endereços de origem e destino configurados. Um deles deve ser configurado como coordenador e o outro como roteador.

## Pinagem

Para estabelecer a comunicação serial, foi utilizado o XBEE Explorer, que possui as portas `RST, RX, TX, GND e 5V`. No arduino, a porta `10` foi utilizada como `TX` e a porta `11` como `RX`.

Ambos coordenadores e roteadores devem ser conectados ao Arduíno da seguinte forma:

| XBEE | Arduino |
|------|---------|
| 5V   | 5V      |
| GND  | GND     |
| RX   | 11 (RX) |
| TX   | 10 (TX) |

Note que as portas `RX` e `TX` do XBEE devem ser conectadas às portas `TX` e `RX` do Arduino, respectivamente, para os dois módulos.