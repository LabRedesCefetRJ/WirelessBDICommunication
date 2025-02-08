import serial
import time
import os

# Configurações
MSG_SIZE = 128
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
TIMEOUT = 10
N = 10  # Número de medições
MODULE_NAME = "XBEE"  # Nome do módulo de transmissão
TRANSMISSION_DISTANCE = 4  # Distância em metros

# Configurar a porta serial
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

# Variáveis de estatísticas
total_bitrate = 0
best_bitrate = 0
worst_bitrate = float("inf")
failed_attempts = 0

# Loop de medições
for i in range(N):
    # Gerar uma mensagem aleatória
    msg = os.urandom(MSG_SIZE)
    
    # Inicia o contador de tempo
    start_time = time.time()
    
    # Envia a mensagem
    ser.write(msg)
    
    # Aguarda a resposta
    response = b""
    while time.time() - start_time < TIMEOUT:
        response = ser.read(MSG_SIZE)
        if response == msg:
            end_time = time.time()
            break
    
    if response == msg:
        elapsed_time = end_time - start_time
        bitrate = (MSG_SIZE * 8) / elapsed_time  # Bits por segundo
        total_bitrate += bitrate
        best_bitrate = max(best_bitrate, bitrate)
        worst_bitrate = min(worst_bitrate, bitrate)
        print(f"{i+1}/{N} - Sucesso: {bitrate:.2f} bps")
    else:
        failed_attempts += 1
        print(f"{i+1}/{N} - Falha na comunicação!")

# Fechar conexão serial
ser.close()

# Cálculo dos resultados
successful_attempts = N - failed_attempts
average_bitrate = total_bitrate / successful_attempts if successful_attempts > 0 else 0
packet_loss = (failed_attempts / N) * 100

# Criar a mensagem de saída
output = f"""
--- Parâmetros ---
Tamanho da mensagem: {MSG_SIZE} bytes
Porta serial: {SERIAL_PORT}
Baud rate: {BAUD_RATE}
Timeout: {TIMEOUT} s
Número de medições: {N}
Módulo de transmissão: {MODULE_NAME}
Distância de transmissão: {TRANSMISSION_DISTANCE} metros

--- Resultados ---
Média da taxa de transferência: {average_bitrate:.2f} bps
Melhor taxa de transferência: {best_bitrate:.2f} bps
Pior taxa de transferência (não zero): {worst_bitrate:.2f} bps
Percentual de pacotes perdidos: {packet_loss:.2f}%
"""

# Exibir no console
print(output)

# Salvar em arquivo
filename = f"{MODULE_NAME}_{TRANSMISSION_DISTANCE}m_{MSG_SIZE}B.txt"
with open(filename, "w") as file:
    file.write(output)

print(f"Resultados salvos em {filename}")
