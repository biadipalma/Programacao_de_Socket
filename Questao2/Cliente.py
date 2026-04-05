import socket  # Importa o módulo de sockets

# Define o IP do servidor (localhost = mesma máquina)
HOST = 'localhost'

# Porta do servidor (deve ser a mesma do servidor)
PORT = 10439

# Cria o socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor usando IP e porta
client.connect((HOST, PORT))

# Loop para manter o chat ativo
while True:
    # Solicita mensagem do usuário
    msg = input("Cliente: ")

    # Envia a mensagem para o servidor
    client.send(msg.encode())

    # Se o cliente digitar QUIT, encerra
    if msg == "QUIT":
        break

    # Recebe resposta do servidor
    resposta = client.recv(1024).decode()

    # Exibe a resposta recebida
    print("Servidor:", resposta)

    # Se o servidor enviar QUIT, encerra
    if resposta == "QUIT":
        break

# Fecha a conexão com o servidor
client.close()