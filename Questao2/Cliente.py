import socket
import os

# Configurações - Substitua pelo seu TIA conforme o roteiro [cite: 23]
HOST = '0.0.0.0'
PORT = 10439  # Primeiros 5 números do seu TIA

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Servidor aguardando conexão na porta {PORT}...")

conn, addr = server.accept()
print(f"Conectado por: {addr}")

while True:
    try:
        # Recebe a opção do menu
        opcao = conn.recv(1024).decode()

        if not opcao or opcao == "3":
            print("Cliente encerrou a conexão.")
            break

        # Opção 1: Receber Mensagem (Chat) [cite: 22]
        elif opcao == "1":
            msg = conn.recv(1024).decode()
            print(f"Cliente: {msg}")
            
            resposta = input("Digite a resposta para o Cliente: ")
            conn.send(resposta.encode())

        # Opção 2: Receber Arquivo [cite: 28, 29]
        elif opcao == "2":
            # Recebe o cabeçalho (nome:tamanho)
            header = conn.recv(1024).decode()
            nome_arquivo, tamanho_arquivo = header.split(":")
            tamanho_arquivo = int(tamanho_arquivo)
            
            nome_limpo = "recebido_" + nome_arquivo.split("/")[-1]
            print(f"Recebendo arquivo: {nome_limpo} ({tamanho_arquivo} bytes)")

            bytes_recebidos = 0
            with open(nome_limpo, "wb") as f:
                while bytes_recebidos < tamanho_arquivo:
                    # Lê apenas o que falta ou o buffer de 1024
                    restante = tamanho_arquivo - bytes_recebidos
                    dados = conn.recv(min(1024, restante))
                    if not dados:
                        break
                    f.write(dados)
                    bytes_recebidos += len(dados)
            
            print(f"Arquivo {nome_limpo} salvo com sucesso!")

    except Exception as e:
        print(f"Erro na conexão: {e}")
        break

conn.close()
server.close()