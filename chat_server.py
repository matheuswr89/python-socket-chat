from database import *
import socket, threading, sys

criarTabelas()

# Verifica se o nome e os argumentos foram corretamente entrados
if(len(sys.argv) < 2) :
    print('Uso: python chat_server.py PORT')
    sys.exit()
# Verifica se a porta é um numero inteiro
try:
    PORT = int(sys.argv[1])
except:
    print('Forneça uma porta!')
    sys.exit()

#inicia o socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

#pegando o ip atual da maquina
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
print("Meu ip é: "+host)

#associando o host e a porta
server.bind((host, PORT))                                   
server.listen()
print("Server inicializado na porta " + str(PORT))

clients = []
nicknames = []

#função para procurar o nickname
def procuraNickname(nick):
    if nicknames == []:
        return -1
    else:                                 
        for nickname in nicknames:
            if(nickname==nick):
                return 0
            else:
                return -1

#função de transmissão
def broadcast(message):                                 
    for client in clients:
        client.send(message)

def handle(client):       
    while True:
        #verifica se recebe uma mensagem de um usuario valido
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
            broadcast('{} saiu da conversa!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

#permite o acesso de varios usuarios
def receive():
    while True:
        client, address = server.accept()
        print("Conectado com {}".format(str(address)))       
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(4096).decode('utf-8')
        senha = client.recv(4096).decode('utf-8')
        #verifica se o usuario existe
        if verificaUser(nickname, senha) == 0:
            #procura o nickname do usuario
            if(procuraNickname(nickname) == -1):
                nicknames.append(nickname)
                clients.append(client)
                print("Seu nickname {}".format(nickname))
                broadcast("{} entrou!".format(nickname).encode('utf-8'))
                mensagens = getMensagens()
                for i in mensagens:
                    client.send(str(i).encode('utf-8'))
                client.send('\n\nDigite \'exit\' para sair da conversa!'.encode('utf-8'))
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            else:
                client.send('-2'.encode('utf-8'))
                client.close()    
        else: 
            client.send('-1'.encode('utf-8'))
            client.close()

#verifica se o usuario existe            
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

