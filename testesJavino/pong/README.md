# Ecoador (o Pong do ping-pong)

Este ecoador simplesmente recebe qualquer mensagem que chegar na porta definida na variável `porta`:

```py
porta = "/dev/ttyUSB1" 
```

Após isso, o ecoador imediatamente envia a mensagem de volta para a mesma porta.

## Como rodar?

Para rodar, navegue com o terminal até este diretório e rode o seguinte comando

```sh
sudo ./runPong.sh
```

Qualquer mensagem recebida ou erro de recebimento serão exibidos no terminal. Por ser o código de comportamento "passivo", os dados são apresentados de forma menos elaborada.