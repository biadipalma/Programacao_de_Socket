import socket          #(cliente-servidor)
import threading       # Permite múltiplos clientes ao mesmo tempo
import random          # Usado para gerar frutas aleatórias
from datetime import datetime  # Para registrar data no histórico
import os              # Para verificar se arquivos existem

# Configuração do servidor
HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 10439      # Porta do servidor

# Listas de frutas dos jogos
frutas1 = ["maca", "banana", "uva", "laranja", "manga"]  # jogo 1
frutas2 = ["🍎", "🍐", "🍋", "🍒", "💎"]                 # jogo 2 

# Lock para evitar conflitos entre threads
lock = threading.Lock()

# Gera sequência secreta para o jogo das frutas
sequencia = [random.choice(frutas1) for _ in range(3)]

# Dicionários para armazenar dados
saldo = {}    # saldo de moedas por jogador

# FUNÇÕES DE ARQUIVO
# Salva saldo em arquivo
def salvar_saldo():
    with open("saldo.txt", "w") as f:
        for nome, valor in saldo.items():
            f.write(f"{nome}:{valor}\n")

# Carrega saldo do arquivo
def carregar_saldo():
    if os.path.exists("saldo.txt"):
        with open("saldo.txt", "r") as f:
            for linha in f:
                nome, valor = linha.strip().split(":")
                saldo[nome] = int(valor)

# Salva histórico de partidas
def salvar_historico(msg):
    with open("historico.txt", "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")


# JOGO 1 - FRUTAS 🍓
def jogo_sequencia(conn, nome):
    global sequencia

    # Mensagem inicial
    conn.send("\n🍓 JOGO DAS FRUTAS\nDigite 'SAIR' para voltar\n".encode())

    tentativas = 0  # contador de rodadas

    while True:
        # Recebe tentativa do jogador
        tentativa_str = conn.recv(1024).decode().strip()

        # Se quiser sair do jogo
        if tentativa_str.upper() == "SAIR":
            conn.send("Voltando ao menu...\n".encode())
            break

        tentativa = tentativa_str.split()
        tentativas += 1

        # Validação
        if len(tentativa) != 3:
            conn.send("Digite 3 frutas!\n".encode())
            continue

        # Verifica tentativa
        resposta = []
        for i in range(3):
            if tentativa[i] == sequencia[i]:
                resposta.append("✅")   # posição correta
            elif tentativa[i] in sequencia:
                resposta.append("🔁")   # fruta certa, posição errada
            else:
                resposta.append("❌")   # fruta não existe

        # Envia resultado para o cliente
        conn.send(f"Resultado: {' '.join(resposta)}\n".encode())

        # Se acertou
        if tentativa == sequencia:
            conn.send(f"\n🎉 VOCÊ VENCEU em {tentativas} rodadas!\n".encode())

            # Atualiza saldo (+20 moedas)
            saldo[nome] = saldo.get(nome, 100) + 20
            salvar_saldo()

            # Salva histórico
            salvar_historico(
                f"{nome} frutas: VENCEU +20 moedas | Rodadas: {tentativas} | Saldo: {saldo[nome]}"
            )

            # Gera nova sequência
            with lock:
                sequencia = [random.choice(frutas1) for _ in range(3)]

            conn.send("🔄 Novo jogo iniciado ou digite SAIR\n".encode())
            tentativas = 0

# JOGO 2 - CASSINO 🎰
def jogo_cassino(conn, nome):
    # Se jogador não tem saldo, inicia com 100
    if nome not in saldo:
        saldo[nome] = 100

    conn.send(f"\n🎰 CASSINO\nSaldo: {saldo[nome]}\nDigite JOGAR ou QUIT\n".encode())

    while True:
        comando = conn.recv(1024).decode().strip().upper()

        # Voltar ao menu
        if comando == "QUIT":
            conn.send("Voltando ao menu...\n".encode())
            break

        # Jogar
        if comando == "JOGAR":
            resultado = [random.choice(frutas2) for _ in range(3)]
            linha = " | ".join(resultado)

            # Verifica vitória
            if resultado[0] == resultado[1] == resultado[2]:
                saldo[nome] += 50
                msg = f"[{linha}] JACKPOT! +50 moedas"
            else:
                saldo[nome] -= 10
                msg = f"[{linha}] Perdeu -10 moedas"

            salvar_saldo()

            # Salva histórico
            salvar_historico(f"{nome} cassino: {msg} | Saldo: {saldo[nome]}")

            # Envia resultado
            conn.send(f"{msg}\nSaldo: {saldo[nome]}\n".encode())

# ========================
# MENU DO CLIENTE
# ========================
def handle_client(conn, addr):
    try:
        # Pede nome do jogador
        conn.send("Digite seu nome:\n".encode())
        nome = conn.recv(1024).decode().strip()

        while True:
            # Menu principal
            conn.send(
                "\n🎮 MENU:\n"
                "1 - Jogo das frutas 🍓\n"
                "2 - Cassino 🎰\n"
                "0 - Sair\n"
                "Escolha:\n".encode()
            )

            escolha = conn.recv(1024).decode().strip()

            # Direciona para o jogo escolhido
            if escolha == "1":
                jogo_sequencia(conn, nome)

            elif escolha == "2":
                jogo_cassino(conn, nome)

            elif escolha == "0":
                conn.send("Saindo...\n".encode())
                break

            else:
                conn.send("Opção inválida!\n".encode())

    except:
        pass

    conn.close()

# ========================
# INICIALIZAÇÃO DO SERVIDOR
# ========================

# Carrega dados salvos
carregar_saldo()

# Cria socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa IP e porta
server.bind((HOST, PORT))

# Começa a escutar conexões
server.listen()

print("Servidor rodando...")

# Loop principal (aceita clientes)
while True:
    conn, addr = server.accept()
    print(f"Cliente conectado: {addr}")

    # Cria uma thread para cada cliente
    threading.Thread(target=handle_client, args=(conn, addr)).start()