import serial
import time
import os

# Configurações
MSG_SIZE = 32
SERIAL_PORT = "/dev/ttyEmulatedPort0"
BAUD_RATE = 9600

# Configurar a porta serial
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

# Gerar uma mensagem aleatória do tamanho especificado
msg = os.urandom(MSG_SIZE)

# Inicia o contador de tempo
start_time = time.time()

# Envia a mensagem aleatória
ser.write(msg)

# Aguarda a resposta
while True:
    response = ser.read(MSG_SIZE)  # Lê a mesma quantidade de bytes
    if response == msg:  # Confirma que a resposta é exatamente igual à enviada
        end_time = time.time()
        break

# Calcula o tempo total e a taxa de transferência
elapsed_time = end_time - start_time
bitrate = (MSG_SIZE * 8) / elapsed_time  # Bits por segundo

print(f"Mensagem enviada ({MSG_SIZE} bytes): {msg.hex()}")
print(f"Mensagem recebida ({MSG_SIZE} bytes): {response.hex()}")
print(f"Tempo decorrido: {elapsed_time:.6f} segundos")
print(f"Taxa de transferência: {bitrate:.2f} bps")

ser.close()
