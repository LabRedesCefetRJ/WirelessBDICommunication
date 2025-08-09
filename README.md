# Comunicação wireless entre arduinos 
Conjunto de códigos Arduíno para realizar a comunicação sem fio usando diferentes módulos e frequências

    - XBEE
    - RF
    - LoRa
    - HC-05
    - BLE
    - NRF24L01

Cada um possui uma pasta dedicada a explicar a sua configuração, pinagem e código de interfaceamento USB/Transmissor (aqui chamado de _ping-pong_). Todos os códigos _ping-pong_ estão presentes também na pasta `ping-pong`.

A pasta `testesJavino` possui os códigos que servem para medir o tempo de ida e volta (RTT: _round-trip-time_). Um deles é apenas um ecoador (`testesJavino/pong/pong.py`), e o outro (`testesJavino/ping/ping.py`) é responsável pelo envio, medição e geração dos arquivos de resultado, salvos em `testesJavino/ping/results`.