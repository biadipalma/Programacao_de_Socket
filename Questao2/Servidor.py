import socket  # Importa o módulo de sockets para comunicação em rede

# Define o IP do servidor
# '0.0.0.0' significa que o servidor aceita conexões de qualquer IP
HOST = '0.0.0.0'

# Porta baseada no TIA (primeiros 5 dígitos)
PORT = 10439

# Cria o socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao IP e porta definidos
server.bind((HOST, PORT))

# Coloca o servidor em modo de escuta
# O número 1 indica o número máximo de conexões pendentes
server.listen(1)

print("Servidor aguardando conexão...")

# Aceita uma conexão de cliente
# conn = conexão com o cliente
# addr = endereço do cliente
conn, addr = server.accept()
print("Conectado por:", addr)

# Loop para manter o chat funcionando
while True:
    # Recebe mensagem do cliente (até 1024 bytes)
    msg = conn.recv(1024).decode()

    # Se o cliente digitar QUIT, encerra a conexão
    if msg == "QUIT":
        print("Cliente encerrou a conexão.")
        break

    # Exibe a mensagem recebida
    print("Cliente:", msg)

    # Pede uma resposta do servidor
    resposta = input("Servidor: ")

    # Envia a resposta para o cliente
    conn.send(resposta.encode())

    # Se o servidor digitar QUIT, encerra
    if resposta == "QUIT":
        break

# Fecha a conexão com o cliente
conn.close()

# Fecha o servidor
server.close()