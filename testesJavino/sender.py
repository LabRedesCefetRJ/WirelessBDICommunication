import javino
import time

TIMEOUT = 3

if __name__ == "__main__":
    porta = "/dev/ttyUSB0"  # Substitua pela porta serial desejada
    comm = javino.start(porta)
    
    if comm:
        while True:
            try:
                javino.addPercept("valores")
                javino.sendPercepts(comm)
                start_time = time.time()
                while time.time() - start_time < TIMEOUT:
                    # Verifica se há mensagens disponíveis na porta serial
                    if javino.availableMsg(comm):
                        mensagem = javino.getMsg(comm)
                        print(f"Mensagem: {mensagem}")
            except KeyboardInterrupt:
                javino.disconnect(comm)
            except:
                print("Timeout!")
    else:
        print("Não foi possível conectar à porta serial.")