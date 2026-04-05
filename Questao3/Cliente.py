import socket
import os

HOST = 'localhost'
PORT = 10439

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    print("\n1 - Enviar mensagem")
    print("2 - Enviar arquivo")
    print("3 - Sair")

    opcao = input("Escolha: ")
    client.send(opcao.encode())

    # SAIR
    if opcao == "3":
        break

    # MENSAGEM
    elif opcao == "1":
        msg = input("Digite a mensagem: ")
        client.send(msg.encode())

        resposta = client.recv(1024).decode()
        print("Servidor:", resposta)

    # ARQUIVO
    elif opcao == "2":
        caminho = input("Digite o nome do arquivo: ")

        if not os.path.exists(caminho):
            print("Arquivo não encontrado!")
            continue

        client.send(caminho.encode())

        with open(caminho, "rb") as f:
            while True:
                dados = f.read(1024)
                if not dados:
                    break
                client.send(dados)

        client.send(b"FIM")
        print("Arquivo enviado com sucesso!")

client.close()