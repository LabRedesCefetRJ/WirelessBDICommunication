# Comunicação wireless entre arduinos 
Conjunto de códigos Arduíno para realizar a comunicação sem fio usando diferentes módulos e frequências

- RF
- BLE
- XBEE
- HC-05
- NRF24L01
- LoRa

Cada um possui uma pasta dedicada a explicar a sua configuração, pinagem e código de interfaceamento USB/Transmissor (aqui chamado de _ping-pong_). Todos os códigos _ping-pong_ estão presentes também na pasta `ping-pong`.

A pasta `testesJavino` possui os códigos que servem para medir o tempo de ida e volta (RTT: _round-trip-time_). Um deles é apenas um ecoador (`testesJavino/pong/pong.py`), e o outro (`testesJavino/ping/ping.py`) é responsável pelo envio, medição e geração dos arquivos de resultado, salvos em `testesJavino/ping/results`.

## Resultados

Abaixo serão apresentados os gráficos contendo os resultados de cada teste para os módulos.

- [RF](#rf)
- [BLE](#ble)
- [XBEE](#xbee)
- [HC-05](#hc-05)
- [NRF24L01](#nrf24l01)
- [LoRa](#lora)

### Como interpretar os gráficos

<img width="605" height="340" alt="EXEMPLO-variacao-tamanho-grafico" src="https://github.com/user-attachments/assets/d40bf2e0-c77c-4a67-bf8f-098aec1aec40" />
<img width="605" height="340" alt="EXEMPLO-variacao-distancia-grafico" src="https://github.com/user-attachments/assets/db1c5efb-9a43-4d73-8241-139fa804a281" />


### RF

<img width="646" height="385" alt="RF_2-medias-grafico" src="https://github.com/user-attachments/assets/b454a41f-1189-41be-9fc8-c47187adf58f" />
<img width="646" height="385" alt="RF_2-porcentagem-grafico" src="https://github.com/user-attachments/assets/169f8556-e1be-4ea4-b6bf-b192298f5e6c" />
<img width="646" height="385" alt="RF_2-desv-grafico" src="https://github.com/user-attachments/assets/535ecae8-25c1-4592-86d3-c1aaeb4d3d8e" />

### BLE

<img width="605" height="340" alt="BLE-medias-grafico" src="https://github.com/user-attachments/assets/e87eb899-ffc3-4499-a225-70185723bc4d" />
<img width="605" height="340" alt="BLE-porcentagem-grafico" src="https://github.com/user-attachments/assets/3cbde9f0-991a-42df-8d90-2cab7b01587e" />
<img width="605" height="340" alt="BLE-desv-grafico" src="https://github.com/user-attachments/assets/5f20e597-979d-4e4f-b8e1-d86f717801ec" />

### XBEE

<img width="646" height="385" alt="XBEE-medias-grafico" src="https://github.com/user-attachments/assets/42264e14-87aa-4749-88eb-2e7c124c03a5" />
<img width="646" height="385" alt="XBEE-porcentagem-grafico" src="https://github.com/user-attachments/assets/2c200c7e-876b-423d-873c-061146d416d9" />
<img width="646" height="385" alt="XBEE-desv-grafico" src="https://github.com/user-attachments/assets/389139f4-a0d3-47ca-895e-6be7d61468c4" />

### HC-05

<img width="646" height="385" alt="BLUETOOTH-medias-grafico" src="https://github.com/user-attachments/assets/bf1b7569-fe78-4908-b5a9-157f2a61c561" />
<img width="646" height="385" alt="BLUETOOTH-porcentagem-grafico" src="https://github.com/user-attachments/assets/d3d3d19f-b629-4b08-bcfa-9db2df7e9f3e" />
<img width="646" height="385" alt="BLUETOOTH-desv-grafico" src="https://github.com/user-attachments/assets/a7793328-19c4-4db6-b64d-9efb0fdfe0dd" />

### NRF24L01

<img width="646" height="385" alt="NRF24L01-medias-grafico" src="https://github.com/user-attachments/assets/b2e3c8f0-23c2-4e90-a5cc-a7b84efbbe32" />
<img width="646" height="385" alt="NRF24L01-porcentagem-grafico" src="https://github.com/user-attachments/assets/e9f22fcf-200b-4253-bbb4-394eda709af5" />
<img width="646" height="385" alt="NRF24L01-desv-grafico" src="https://github.com/user-attachments/assets/f533b2f6-7e3f-4cf9-9a99-6d7152af7ed6" />

### LoRa

<img width="646" height="385" alt="LORA-medias-grafico" src="https://github.com/user-attachments/assets/55a66590-adda-419a-94f4-da0a8adfc788" />
<img width="646" height="385" alt="LORA-porcentagem-grafico" src="https://github.com/user-attachments/assets/8773d7f9-4f58-486b-80f1-8f2b951b5470" />
<img width="646" height="385" alt="LORA-desv-grafico" src="https://github.com/user-attachments/assets/b543eb3f-0c5f-4d25-9e08-0126e9bcf51b" />









