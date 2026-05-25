# TRABALHO DE REDES DE COMPUTADORES I (Sockets)
## 👩‍💻 Integrantes
- Thaís Sousa 
- Lorena de Carvalho

 ## 🖥️ Aplicação
 Um jogo da velha que trabalha o uso de sockets por meio da troca de turnos entre dois sistemas finais durante uma partida.
 Nesse caso, temos o cliente (jogador 1), que solicita a conexão e inicia a jogada, e o servidor (jogador 2), que espera e aceita a conexão e, então, 
 após a vez do jogador 1, realiza sua jogada. Dessa forma, cada hospedeiro joga alternadamente e envia mensagens que informam o estado da partida por
 meio dos sockets.


 ## 🚀 Como Executar o Projeto (Cliente/Servidor)

Este projeto consiste em uma aplicação de rede simples utilizando a biblioteca nativa `socket` do Python.

### 📋 Pré-requisitos
* [Python 3](https://python.org) instalado no seu computador.

### 🔧 Como Executar

Para testar a comunicação, você precisará abrir **dois terminais (janelas de comando)** diferentes no seu computador: um para o servidor e outro para o cliente.

#### Passo 1: Iniciar o Servidor
O servidor precisa ser iniciado primeiro para ficar ouvindo e aguardando as conexões. No primeiro terminal, execute:
```bash
python servidor.py
```
*(Nota: O terminal ficará travado/em execução, o que significa que o servidor está ativo).*

#### Passo 2: Iniciar o Cliente
Com o servidor já rodando, abra um segundo terminal na mesma pasta e execute:
```bash
python cliente.py
```

### 💡 Dicas de Teste
* **Na mesma máquina:** Certifique-se de que o arquivo `cliente.py` está configurado para conectar ao IP `127.0.0.1` (localhost).
* **Em máquinas diferentes:** Altere o IP no arquivo do cliente para o IP da rede local da máquina que está rodando o servidor.
