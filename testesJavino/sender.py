import javino

if __name__ == "__main__":
    porta = "/dev/ttyEmulatedPort0"  # Substitua pela porta serial desejada
    comm = javino.start(porta)
    
    if comm:
        try:
            javino.addPercept("valores")
            javino.sendPercepts(comm)
            # while True:
            #     # Verifica se há mensagens disponíveis na porta serial
            #     if javino.availableMsg(comm):
            #         mensagem = javino.getMsg(comm)                   
            #         if mensagem == "getPercepts":
            #             getExogenousPerceptions()
            #             print("sending perceptions")
            #             javino.sendPercepts(comm)
            #         elif mensagem == "ledOn":
            #             ledOn()
            #         elif mensagem == "ledOff":
            #             ledOff()
            #         else:
            #             print(f"Action not implemented:{mensagem}")
        except KeyboardInterrupt:
            javino.disconnect(comm)
    else:
        print("Não foi possível conectar à porta serial.")