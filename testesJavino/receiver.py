import javino

if __name__ == "__main__":
    porta = "/dev/ttyExogenous0"  # Substitua pela porta serial desejada
    comm = javino.start(porta)
    
    if comm:
        try:
            while True:
                # Verifica se há mensagens disponíveis na porta serial
                if javino.availableMsg(comm):
                    mensagem = javino.getMsg(comm)                   
                    javino.addPercept(mensagem)
                    print(f"Received: {mensagem}")
                    javino.sendPercepts(comm)
        except KeyboardInterrupt:
            javino.disconnect(comm)
    else:
        print("Não foi possível conectar à porta serial.")