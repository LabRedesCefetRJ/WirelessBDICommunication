import serial

# Configurações
SERIAL_PORT = "/dev/ttyExogenous0"
BAUD_RATE = 9600

# Configurar a porta serial
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)

while True:
    data = ser.read(256)  # Lê até 128 bytes para suportar mensagens maiores
    if data:
        ser.write(data)  # Envia de volta a mesma mensagem

ser.close()

