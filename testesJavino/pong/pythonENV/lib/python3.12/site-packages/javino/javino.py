import serial
import time

percepts_buffer = []
_strMessage     = ""


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
        ser.flush()
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
        if bytes_available > 0:
            ### Header == fffe
            h = ser.read(1).decode().strip()
            if h != "f":
                return False
            h = ser.read(1).decode().strip()
            if h != "f":
                return False
            h = ser.read(1).decode().strip()
            if h != "f":
                return False
            h = ser.read(1).decode().strip()
            if h != "e":
                return False

            #### Size Message fffeXX where XX is a Hexadecimal value (00 until ff) -- maxpayload=255bytes
            size_decimal = 0
            try:
                size_hex = ser.read(2).decode().strip()
                size_decimal = int(size_hex, 16)
            except:
                return False

            #### Message
            bytesInChannel = ser.in_waiting
            if bytesInChannel < size_decimal:
                print(f"[JAVINO] Incomming message")
                notReceived = size_decimal - bytesInChannel
                timeout = ((0.02*size_decimal)+0.5)
                while ((notReceived > 0) and (timeout > 0)):
                    time.sleep(0.005)
                    timeout = timeout - 0.005
                    bytesInChannel = ser.in_waiting
                    if bytesInChannel < size_decimal:
                        #print(f"Timeout: {timeout}, bytes: {bytesInChannel}", end=" ", flush=True) 
                        notReceived = size_decimal - bytesInChannel 
                        #print(f"NOT RECEIVED: {notReceived}")
                    else:
                        #print(f"arrieved bytes: {bytesInChannel}")
                        #global _strMessage
                        #_strMessage = ser.read(size_decimal).decode().strip()
                        setMsg(ser.read(size_decimal).decode().strip())
                        return True
                print(f"[JAVINO] Timeout: {notReceived} bytes missing")
                clearChannel(ser)
                return False
            else:
                #global _strMessage
                #_strMessage = ser.read(size_decimal).decode().strip()
                setMsg(ser.read(size_decimal).decode().strip())
                return True
        else:
            time.sleep(0.02)
            return False
    except serial.SerialException as e:
        #print(f"Error getting message from serial port: {e}")
        print(f"Error checking available messages: {e}")
        return False


def getMsg():
    global _strMessage 
    output = _strMessage
    _strMessage = None
    return output

def setMsg(msg):
    global _strMessage  
    _strMessage = msg

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

def clearChannel(ser):
    ser.reset_input_buffer()
    #print(f"[JAVINO] Cleanning the Serial Channel...")