import socket, threading, sys

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
#associando o host e a porta
server.bind(('10.8.0.8', PORT))                                   
server.listen()
print("Server inicializado na porta " + str(PORT))

clients = []
nicknames = []

#função de transmissão
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        #verifica se recebe uma mensagem de um usuario valido
        try:
            message = client.recv(4096)
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
        nicknames.append(nickname)
        clients.append(client)
        print("Seu nickname {}".format(nickname))
        broadcast("{} entrou!".format(nickname).encode('utf-8'))
        client.send('Digite \'exit\' para sair da conversa!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()