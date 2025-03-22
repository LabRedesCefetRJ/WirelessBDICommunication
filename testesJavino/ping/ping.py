import javino 
import time 
import random 
import string

sizeOfMsg = 255
porta = "/dev/ttyUSB0"  
comm = javino.start(porta)


def random_message(sm):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=sm))

if comm:
    try:
        while True:
            message = random_message(sizeOfMsg)
            javino.clearChannel(comm)
            javino.sendMsg(comm,message) 
            print(f"sent: {message}", end =" ", flush=True)
            attemp = 200
            while attemp > 0:
                print(".", end =" ", flush=True)
                attemp = attemp -1
                if javino.availableMsg(comm):
                    received = javino.getMsg(comm)
                    if received == message:
                        attemp = 0
                        print(f"received: {received}", end =" ", flush=True)
                    elif received != None:
                        print(f"late: {received}", end =" ", flush=True)
                        javino.clearChannel(comm)
            print("")  
            time.sleep(3)          
    except KeyboardInterrupt:
        javino.disconnect(comm)
else:
    print("Não foi possível conectar à porta serial.")