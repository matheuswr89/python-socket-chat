import socket, threading
nickname = input("Choose your nickname: ")

hostname = socket.gethostname()
host = str(socket.gethostbyname(hostname))                      #get machine intern ip

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((host, 7976))                                    #connecting client to server

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break
def write():
    while True:                                                 #message layout
        message_write = input('Write a message: ')
        message = '{}: {}'.format(nickname, message_write)
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()