import socket

def desenhar_tabuleiro(matriz):
    return f"""
     {matriz[0][0]} | {matriz[0][1]} | {matriz[0][2]} 
    ---|---|---
     {matriz[1][0]} | {matriz[1][1]} | {matriz[1][2]} 
    ---|---|---
     {matriz[2][0]} | {matriz[2][1]} | {matriz[2][2]} 
    """

# Função para verificar se o jogo deu velha (empate)
def deu_velha(matriz):
    linhas = [# Horizontais
        [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
        # Verticais
        [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
        # Diagonais
        [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]]
    
    # Verifica a possibilidade de vitória em cada linha, coluna e diagonal
    for linha in linhas:
        simbolos = [matriz[lin][col] for lin, col in linha]
    
        se_tem_X = "X" in simbolos
        se_tem_O = "O" in simbolos

        # Se uma linha, coluna ou diagonal não tiver os dois símbolos, o jogo ainda não deu velha
        if not(se_tem_X and se_tem_O):
            return False
    return True
        
# Função para verificar se um jogador venceu        
def verificar_vencedor(matriz, jogador):
    for i in range(3):
        if matriz[i][0] == matriz[i][1] == matriz[i][2] == jogador: return True
        if matriz[0][i] == matriz[1][i] == matriz[2][i] == jogador: return True
    if matriz[0][0] == matriz[1][1] == matriz[2][2] == jogador: return True
    if matriz[0][2] == matriz[1][1] == matriz[2][0] == jogador: return True
    return False


# Configurações do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(("0.0.0.0", 50000))

servidor.listen(1)
print("Aguardando conexão...")

conexao, ip_cliente = servidor.accept()
print(f"Cliente de ip {ip_cliente} conectado. \nO jogo vai começar! \nVocê é o jogador 2(X), aguarde a jogada do jogador 1(O)...")

jogar = True

# cliente - jogador 1(O) \ servidor - jogador 2(X)
# cliente que inicia as partidas
while (jogar) :
    matriz =  [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]

    while True :

        # Confere se deu velha antes de iniciar o turno do cliente
        if(deu_velha(matriz)):
            print("Deu velha! Fim de jogo.")
            conexao.send(f"{desenhar_tabuleiro(matriz)}\nDeu velha! Empate técnico.\n".encode('utf-8'))
            break

        mensagem_enviada = (f"Sua vez de jogar, jogador 1 (O): \n {desenhar_tabuleiro(matriz)}")
        conexao.send(mensagem_enviada.encode('utf-8'))


        # Cliente envia a resposta 
        mensagem_recebida = conexao.recv(1024).decode('utf-8')
        if not mensagem_recebida: 
            print("\n[AVISO] O cliente desconectou ou fechou o jogo!")
            break
        linha, coluna = map(int, mensagem_recebida.split(","))

        # Verifica se a jogada do cliente é válida e retorna uma mensagem de erro caso não seja
        if matriz[linha][coluna] == ' ':
            matriz[linha][coluna] = 'O'
            jogada_feita = (f"{desenhar_tabuleiro(matriz)}\nAguardando o jogador 2...")
            conexao.send(jogada_feita.encode('utf-8'))
        else:
            aviso_erro = f"Posição inválida! [{linha},{coluna}] já está ocupada. Tente novamente."
            conexao.send(aviso_erro.encode('utf-8'))
            continue 

        # Verifica se, com a última jogada do cliente, ele ganha o jogo
        venceu = verificar_vencedor(matriz, 'O')

        if venceu:
            print(f"Você perdeu. O jogador 1 ganhou!\n{desenhar_tabuleiro(matriz)}")
            parabens = f"Você venceu!\n{desenhar_tabuleiro(matriz)}"
            conexao.send(parabens.encode('utf-8'))
            break
        
        # Verifica se deu velha antes de iniciar o turno do servidor
        if deu_velha(matriz):
            print(f"Deu velha!\n{desenhar_tabuleiro(matriz)}\nFim de jogo.")
            conexao.send(f"Deu velha!\n{desenhar_tabuleiro(matriz)}\nFim de jogo.".encode('utf-8'))
            break
        
       # Inicia o turno do servidor
        print(f"\nTabuleiro atual: {desenhar_tabuleiro(matriz)}")
        print("Sua vez de jogar, jogador 2 (X):")

        # Recebendo e verificando a jogada do servidor (se é válida ou se a posição já está ocupada)
        while True:
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

            if matriz[linha][coluna] != ' ':
                    print("Posição já ocupada! Tente novamente.")
                    continue       
                
            break
        
        matriz[linha][coluna] = 'X'

        # Verifica se deu velha após a última jogada do servidor
        if deu_velha(matriz):
            print(f"Deu velha!\n{desenhar_tabuleiro(matriz)}\nFim de jogo.")
            conexao.send(f"Deu velha!\n{desenhar_tabuleiro(matriz)}\nFim de jogo.".encode('utf-8'))
            break
        print(f"\nJogada enviada! \n{desenhar_tabuleiro(matriz)}\nAguardando o jogador 1...\n")

        # Verifica se o servidor ganhou o jogo com a sua última jogada
        venceu_servidor = verificar_vencedor(matriz, 'X')

        if venceu_servidor:
            print(f"Você venceu!\n{desenhar_tabuleiro(matriz)}")
            derrota_cliente = f"Você perdeu! O jogador 2 ganhou. \n {desenhar_tabuleiro(matriz)}"
            conexao.send(derrota_cliente.encode('utf-8'))
            break

    # Fim do jogo, pergunta se deseja jogar novamente       
    conexao.send("\nVocê deseja jogar novamente? (sim/nao): ".encode('utf-8'))
    resposta_servidor = input("\nVocê deseja jogar novamente? (sim/nao): ").lower()

    try:
        resposta_cliente = conexao.recv(1024).decode('utf-8').lower()
    except:
        resposta_cliente = "nao"
        
    if resposta_servidor == 'sim' and resposta_cliente == 'sim':
            print("Nova partida iniciando... Aguarde a jogada do jogador 1(O)...")
            jogar = True
    else:
            print("Fim do jogo!")
            jogar = False

# Fim do loop principal do jogo, encerrando a conexão
conexao.close()
servidor.close()
print("Conexão encerrada.")