import javino 
import time 
import random 
import string
import json
from pathlib import Path

porta = "/dev/ttyUSB0"  
comm = javino.start(porta)

# Donfigurações
QTD_MEDICOES = 1
TIMEOUT = 1
INTERVAL_BETWEEN_MEASUREMENTS = 1
MESSAGE_SIZE = [16, 32, 64, 128, 255]  # Tamanhos de mensagem em bytes
MODULE_NAME = "TESTE"  # Nome do módulo de transmissão
TRANSMISSION_DISTANCE = 32  # Distância em metros

# Show configurations
print(f"Number of measurements: {QTD_MEDICOES}")
print(f"Timeout: {TIMEOUT} s")
print(f"Interval between measurements: {INTERVAL_BETWEEN_MEASUREMENTS} s")
print(f"Transmission distance: {TRANSMISSION_DISTANCE} m")
print(f"Message sizes: {MESSAGE_SIZE}")
print(f"Module: {MODULE_NAME}")
print("\n=================================================\n")  

# Json para guardar as configurações e array de resultados para cada tamanho de mensagem
results = {
    "module": MODULE_NAME,
    "distance": TRANSMISSION_DISTANCE,
    "message_sizes": MESSAGE_SIZE,
    "timeout": TIMEOUT,
    "interval": INTERVAL_BETWEEN_MEASUREMENTS,
    "results": []
}

# Função para gerar uma mensagem aleatória
def random_message(sm):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=sm))


if comm:
    try:
        message = random_message(1)
        javino.clearChannel(comm)

        javino.sendMsg(comm,message) 
        time.sleep(15)
        for sizeOfMsg in MESSAGE_SIZE:
            print("\n=================================================\n")

            # Variáveis de estatísticas
            total_elapsed = 0
            best_elapsed = 0
            worst_elapsed = float("inf")
            failed_attempts = 0
            measurements = []

            for i in range(QTD_MEDICOES):
                print(f"\n{MODULE_NAME}: Attempt {i+1}/{QTD_MEDICOES}, ({sizeOfMsg} bytes)")
                message = random_message(sizeOfMsg)
                javino.clearChannel(comm)

                start_time = time.time()

                javino.sendMsg(comm,message) 
                # print(f"sent: \x1b[33m{message}\x1b[0m", end =" \n", flush=True)

                success = False
                while time.time() - start_time <= TIMEOUT and success == False:
                    print(".", end ="", flush=True)
                    if javino.availableMsg(comm):
                        print("")  
                        received = javino.getMsg()
                        if received == message:
                            end_time = time.time()
                            elapsed_time = (end_time - start_time) * 1000
                            success = True
                            total_elapsed += elapsed_time
                            measurements.append(elapsed_time)
                            best_elapsed = max(best_elapsed, elapsed_time)
                            worst_elapsed = min(worst_elapsed, elapsed_time)
                            print(f"Received (\x1b[42m{elapsed_time:.2f}\x1b[0m ms): \x1b[32m{received}\x1b[0m", end =" ", flush=True)
                        elif received != None:
                            print(f"Late: {received}", end =" ", flush=True)
                            javino.clearChannel(comm)
                        elif received == None:
                            print("\x1b[31mPacket Lost\x1b[0m", end =" ", flush=True)
                if not success:
                    failed_attempts += 1
                    print("\x1b[31mTimeout\x1b[0m", end =" ", flush=True)
                print("\n\n=================================================\n")  
                time.sleep(INTERVAL_BETWEEN_MEASUREMENTS)    

            # Estatísticas
            print(f"Size of message: {sizeOfMsg} bytes")
            if QTD_MEDICOES - failed_attempts > 0:
                print(f"Average elapsed time: {total_elapsed / (QTD_MEDICOES - failed_attempts):.2f} ms")
            else:
                print("Average elapsed time: N/A")
            print(f"Best elapsed time: {best_elapsed:.2f} ms")
            print(f"Worst elapsed time: {worst_elapsed:.2f} ms")
            print(f"Failed attempts: {failed_attempts}")
            print(f"Success rate: {(QTD_MEDICOES - failed_attempts) / QTD_MEDICOES * 100:.2f}%")
            print(f"Measurements: {measurements}")

            # Salvar os resultados
            results["results"] = {
                "message_size": sizeOfMsg,
                "average_elapsed": total_elapsed / (QTD_MEDICOES - failed_attempts) if QTD_MEDICOES - failed_attempts > 0 else 0,
                "best_elapsed": best_elapsed,
                "worst_elapsed": worst_elapsed,
                "failed_attempts": failed_attempts,
                "success_rate": (QTD_MEDICOES - failed_attempts) / QTD_MEDICOES * 100,
                "measurements": measurements
            }
            # Salvar em arquivo
            dir = Path(f"results/{MODULE_NAME}/{TRANSMISSION_DISTANCE}m")
            filename = f"{sizeOfMsg}B.txt"
            filepath = dir / filename
            dir.mkdir(parents=True, exist_ok=True)

            filepath.write_text(json.dumps(results))

            print(f"Resultados salvos em results/{MODULE_NAME}/{TRANSMISSION_DISTANCE}m/{filename}")
    except KeyboardInterrupt:
        javino.disconnect(comm)
else:
    print("Não foi possível conectar à porta serial.")


javino.disconnect(comm)