
import socket

# Criando o socket do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 50000

print(f"Tentando se conectar ao servidor {IP_SERVIDOR} na porta {PORTA_SERVIDOR}...")

cliente.connect((IP_SERVIDOR, PORTA_SERVIDOR))
print("Conectado com sucesso! Você é o jogador 1(O)")

# Loop para receber mensagens do servidor e enviar jogadas
while True:
    resposta_servidor = cliente.recv(1024).decode('utf-8')
    # Se o servidor fechar a conexão ou enviar uma mensagem vazia, encerra o loop
    if not resposta_servidor:
        break
        
    print(resposta_servidor)
    
    # Verificando mensagens específicas do servidor para orientar o cliente
    if "venceu" in resposta_servidor or "perdeu" in resposta_servidor or "velha" in resposta_servidor:
        print("A partida terminou. Aguardando decisão de reiniciar...")
        continue    

    if "Sua vez de jogar, jogador 1 (O)" in resposta_servidor:

        # Recebendo e verificando a jogada do cliente
        while True:
                    try:
                        linha = int(input("Escolha a linha (0-2): "))
                        if 0 <= linha <= 2:
                            break  # Número correto! Sai do loop da linha e vai para a coluna
                        print("Linha inválida! Digite um número entre 0 e 2.")
                    except ValueError:
                        print("Entrada inválida! Digite apenas números inteiros.")
        while True:
                    try:
                        coluna = int(input("Escolha a coluna (0-2): "))
                        if 0 <= coluna <= 2:
                            break  # Número correto! Sai do loop da coluna
                        print("Coluna inválida! Digite um número entre 0 e 2.")
                    except ValueError:
                        print("Entrada inválida! Digite apenas números inteiros.")        
        
        jogada = f"{linha},{coluna}"
        cliente.send(jogada.encode('utf-8'))

        # Verificando se o servidor respondeu com uma mensagem de posição inválida
        if "Posição inválida" in resposta_servidor:
            print("⚠️ Atenção: digite uma posição que esteja vazia no tabuleiro!")
            continue

        print("\nJogada enviada!\n")
    
    # Determina se o cliente deseja jogar novamente ou não
    elif "deseja jogar novamente" in resposta_servidor:
        opcao = input("Digite sim ou nao: ").lower()
        cliente.send(opcao.encode('utf-8'))
        
        if opcao != "sim":
            break
# Fim do jogo e desconectando
cliente.close()
print("Conexão encerrada.")
