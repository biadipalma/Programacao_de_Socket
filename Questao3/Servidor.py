import socket
import os

HOST = '0.0.0.0'
PORT = 10439

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Servidor aguardando conexão...")

conn, addr = server.accept()
print("Conectado por:", addr)

while True:
    opcao = conn.recv(1024).decode()

    # ENCERRAR
    if opcao == "3":
        print("Cliente encerrou.")
        break

    # RECEBER MENSAGEM
    elif opcao == "1":
        msg = conn.recv(1024).decode()
        print("Cliente:", msg)

        resposta = input("Servidor: ")
        conn.send(resposta.encode())

    # RECEBER ARQUIVO
    elif opcao == "2":
        nome_arquivo = conn.recv(1024).decode()
        print("Recebendo arquivo:", nome_arquivo)

        with open("recebido_" + nome_arquivo, "wb") as f:
            while True:
                dados = conn.recv(1024)
                if dados == b"FIM":
                    break
                f.write(dados)

        print("Arquivo recebido com sucesso!")

conn.close()
server.close()