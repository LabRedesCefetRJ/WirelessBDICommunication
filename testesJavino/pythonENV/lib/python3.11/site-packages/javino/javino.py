import serial
import time

percepts_buffer = []

def start(port, baudrate=9600):
    try:
        # Initialize communication with the serial port
        ser = serial.Serial(port, baudrate)
        print(f"Connected to serial port {port}")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to serial port {port}: {e}")
        return None

def listen(ser):
    try:
        # Read available bytes from the serial port
        bytes_available = ser.in_waiting
        if bytes_available > 0:
            line = ser.read(bytes_available).decode().strip()
            if line.startswith("fffe"):
                size_hex = line[4:6]
                size_decimal = int(size_hex, 16)
                data = line[6:6+size_decimal]
                return data
        return None
    except serial.SerialException as e:
        print(f"Error reading from serial port: {e}")
        return None

def sendMsg(ser, message):
    try:
        # Format the response message
        response = "fffe" + format(len(message), '02x') + message
        ser.write(response.encode())
    except serial.SerialException as e:
        print(f"Error writing to serial port: {e}")

def disconnect(ser):
    try:
        ser.close()
        print("Disconnected from serial port.")
    except AttributeError:
        print("No serial port connected.")

def availableMsg(ser):
    try:
        # Check if there are available bytes in the serial port
        bytes_available = ser.in_waiting
        #return bytes_available > 0
        if bytes_available > 0:
            return True
        else:
            time.sleep(0.05)
            return False
    except serial.SerialException as e:
        print(f"Error checking available messages: {e}")
        return False

def getMsg(ser):
    try:
        # Read available bytes from the serial port
        bytes_available = ser.in_waiting
        if bytes_available > 0:
            line = ser.read(bytes_available).decode().strip()
            if line.startswith("fffe"):
                size_hex = line[4:6]
                size_decimal = int(size_hex, 16)
                data = line[6:6+size_decimal]
                return data
        return None
    except serial.SerialException as e:
        print(f"Error getting message from serial port: {e}")
        return None

def addPercept(percept):
    # Adiciona o percept ao buffer
    percepts_buffer.append(percept)

def sendPercepts(ser):
    try:
        # Envia os percepts armazenados no buffer
        if percepts_buffer:
            # Concatena todos os percepts em uma única string separada por ;
            percepts_string = ";".join(percepts_buffer) + ";"
            percepts_buffer.clear()
            sendMsg(ser,percepts_string)
        else:
            print("Without perceptions to send!")
    except serial.SerialException as e:
        print(f"Erro ao enviar percepts pela porta serial: {e}")
