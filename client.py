from database import *
import socket, threading,sys

# Verifica se o nome e os argumentos foram corretamente entrados
if(len(sys.argv) < 3) :
    print('Uso: python client.py SERVER-IP PORT')
    sys.exit()
    
host = sys.argv[1]
# Verifica se a porta é um numero inteiro
try:
    port = int(sys.argv[2])
except:
    print('Forneça a porta do servidor')
    sys.exit()

#verifica se é possivel conectar com o servidor
try:
    #inicia o socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #conecta o usuario ao servidor
    client.connect((host, port))
except:
    print('Erro ao conectar com o servidor')
    sys.exit()

nickname = input("Escolha o seu nickname: ")
senha = input("Forneça a senha: ")

retorno = getUsuario(nickname,senha)
if(retorno == []):
    insertUsuario(nickname,senha)
idUsuario = getUsuario(nickname,senha)[0][0]

#printa todas as mensagens guardado no banco de dados na tela
getMensagens()

# fazendo uma conexão valida
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            if message != 'exit':
                print("Bye bye!")
            else:
                print("Um erro ocorreu!")
                client.close()
            break
    
#layout da mensagem
def write():
    while True:
        message_write = input('')
        if message_write == 'exit':
            client.close()
            sys.exit()
        else:
            message = '{}: {}'.format(nickname, message_write)
            client.send(message.encode('utf-8'))
            insertMensagem(message_write,idUsuario)
#recebendo varias mensagens
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#enviando mensagens
write_thread = threading.Thread(target=write) 
write_thread.start()