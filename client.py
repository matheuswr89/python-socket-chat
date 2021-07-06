import socket, threading, sys

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
print('\n')
# fazendo uma conexão valida
def receive():
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
                client.send(senha.encode('utf-8'))
            else:
                print(message)
        except:
            print("Bye bye!")
            break
    
#layout da mensagem
def write():
    while True:
        message_write = input('')
        sys.stdout.flush()
        if(message_write != ''):
            if message_write == 'exit':
                client.close()
                exit()
            else:
                message = '{}: {}'.format(nickname, message_write)
                client.send(message.encode('utf-8'))

#recebendo varias mensagens
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# valida se os dados de login estão corretos ou
# se o usuario já está logado
id = client.recv(4096).decode('utf-8')
if id==str(-1) or id==str(-2):
    if id==str(-1):
        print("\nDados de login incorretos!")
    else:
        print("\nUsuario já logado!")
    client.close()
    sys.exit(0)
else:
    #enviando mensagens
    write_thread = threading.Thread(target=write) 
    write_thread.start()