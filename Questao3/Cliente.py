import socket
import threading

HOST = '127.0.0.1'
PORT = 10439

# Recebe mensagens do servidor
def receber(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

# Envia mensagens para o servidor
def enviar(sock):
    while True:
        try:
            msg = input()
            sock.send(msg.encode())
        except:
            break

# Cria socket cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client.connect((HOST, PORT))

# Thread para receber mensagens
threading.Thread(target=receber, args=(client,)).start()

# Thread para enviar mensagens
threading.Thread(target=enviar, args=(client,)).start()