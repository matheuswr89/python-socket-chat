from database import *
import socket
import ssl
import threading
import sys

f = open('caminho-certificado.txt', 'r')
linhas = f.read().split('\n')
CERT_FILE = linhas[0]
KEY_FILE = linhas[1]
f.close()

# Verifica se o nome e os argumentos foram corretamente entrados
if(len(sys.argv) < 2):
    print('\n\nUso: python server.py PORT\n\n')
    sys.exit()
# Verifica se a porta é um numero inteiro
try:
    PORT = int(sys.argv[1])
except:
    print('\n\nForneça uma porta!\n\n')
    sys.exit()

host = socket.gethostbyname(socket.gethostname())
print("Meu servidor: "+host+":"+str(PORT))

# inicia o socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# associando o host e a porta
server.bind((host, PORT))
server.listen()

criarTabelas()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERT_FILE,
                        keyfile=KEY_FILE)
serverSocket_ssl = context.wrap_socket(server, server_side=True)

clients = []
nicknames = []

# função para procurar o nickname


def procuraNickname(nick):
    if nicknames == []:
        return -1
    else:
        for nickname in nicknames:
            if(nickname == nick):
                return 0
            else:
                return -1

# função de transmissão


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        # verifica se recebe uma mensagem de um usuario valido
        try:
            message = client.recv(4096)
            insertMensagem(message)
            broadcast(message)
        except:
            # exclui um usuario
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print('{} saiu.'.format(nickname))
            broadcast('{} saiu da conversa!\n'.format(
                nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# permite o acesso de varios usuarios


def receive():
    while True:
        try:
            connectionSocket, addr = serverSocket_ssl.accept()
            print("Conectado com {}:{}".format(str(addr)))
            connectionSocket.send('NICKNAME'.encode('utf-8'))
            nickname = connectionSocket.recv(4096).decode('utf-8')
            senha = connectionSocket.recv(4096).decode('utf-8')
            # verifica se o usuario existe
            if verificaUser(nickname, senha) == 0:
                # procura o nickname do usuario
                if(procuraNickname(nickname) == -1):
                    nicknames.append(nickname)
                    clients.append(connectionSocket)
                    print("Seu nickname {}".format(nickname))
                    broadcast("{} entrou!\n".format(nickname).encode('utf-8'))
                    mensagens = getMensagens()
                    connectionSocket.send(mensagens.encode('utf-8'))
                    thread = threading.Thread(
                        target=handle, args=(connectionSocket,))
                    thread.start()
                else:
                    connectionSocket.send('-2'.encode('utf-8'))
                    connectionSocket.close()
            else:
                connectionSocket.send('-1'.encode('utf-8'))
                connectionSocket.close()
        except:
            print('O endereço {} saiu.'.format(addr))

# verifica se o usuario existe


def verificaUser(nickname, senha):
    retorno = getUsuarioName(nickname)
    if retorno == None:
        insertUsuario(nickname, senha)
        return 0
    else:
        if retorno[0] == senha:
            return 0
        else:
            return -1


receive()
