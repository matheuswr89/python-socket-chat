from tkinter import messagebox, Frame, Tk, Text, Label, Button, Scrollbar, END, VERTICAL, Entry, StringVar
import socket
import ssl
import threading
import sys

f = open('caminho-certificado.txt', 'r')
linhas = f.read().split('\n')
CERT_FILE = linhas[0]
f.close()

# Verifica se o nome e os argumentos foram corretamente entrados
if(len(sys.argv) < 3):
    print('\n\nUso: python client.py SERVER-IP PORT\n\n')
    sys.exit()

host = sys.argv[1]
# Verifica se a porta é um numero inteiro
try:
    port = int(sys.argv[2])
except:
    print('\n\nForneça a porta do servidor.\n\n')
    sys.exit()

# verifica se é possivel conectar com o servidor
try:
    # inicia o socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT_FILE)
    clientSocket_ssl = context.wrap_socket(client, server_hostname=host)
    clientSocket_ssl.connect((host, port))
except:
    print('\n\nErro ao conectar com o servidor\n\n')
    sys.exit()

# fazendo uma conexão valida


def receive():
    while True:
        try:
            message = clientSocket_ssl.recv(4096)
            chat_transcript_area.insert('end', message.decode('utf-8'))
            chat_transcript_area.yview(END)
        except Exception as error:
            print(error)
            if error.args[0] == 10054:
                clientSocket_ssl.close()
                root.destroy()
                break
            break
    exit(0)

# verifica se os dados de login foram entrados corretamente


def login_verify():
    global nickname, senha
    nickname = username_verify.get()
    senha = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    if nickname == '' or senha == '':
        messagebox.showerror("Erro", "Os campos não pode ficar vazios.")
    else:
        message = clientSocket_ssl.recv(4096).decode('utf-8')
        if message == 'NICKNAME':
            clientSocket_ssl.send(nickname.encode('utf-8'))
            clientSocket_ssl.send(senha.encode('utf-8'))

        # valida se os dados de login estão corretos ou
        # se o usuario já está logado
        id = clientSocket_ssl.recv(4096).decode('utf-8')
        if id == str(-1) or id == str(-2):
            if id == str(-1):
                messagebox.showerror("Erro", "Dados de login invalidos.")
            else:
                messagebox.showerror("Erro", "Usuario já logado.")
            login_screen.destroy()
            clientSocket_ssl.close()
            sys.exit(0)
        else:
            login_screen.destroy()
            writeGUI()

# verifica se foi apertado a tecla enter


def on_enter_key_pressed(event):
    sendChat()
    clear_text()

# limpa o texto do componente text


def clear_text():
    enter_text_widget.delete(1.0, 'end')

# monta o layout da mensagem e o envia


def sendChat():
    data = enter_text_widget.get(1.0, 'end').strip()
    if data != '':
        message = '{}: {}\n'.format(nickname, data)
        clientSocket_ssl.send(message.encode('utf-8'))

# GUI do chat


def writeGUI():
    global root, chat_transcript_area, enter_text_widget
    root = Tk()
    root.title("Chat")
    root.protocol("WM_DELETE_WINDOW", on_closing_chat)
    frame = Frame(root)
    Label(frame, text='Chat Box:',
          font=("Serif", 12)).pack(side='top')
    chat_transcript_area = Text(
        frame, width=60, height=10, font=("Serif", 12))
    scrollbar = Scrollbar(
        frame, command=chat_transcript_area.yview, orient=VERTICAL)
    chat_transcript_area.config(yscrollcommand=scrollbar.set)
    chat_transcript_area.bind("<Key>", lambda a: "break")
    chat_transcript_area.pack(side='left', padx=10)
    scrollbar.pack(side='right', fill='y')
    frame.pack(side='top')
    Label(root, text='Enter message:',
          font=("Serif", 12)).pack(side='top')
    enter_text_widget = Text(
        root, width=60, height=1, font=("Serif", 12))
    enter_text_widget.focus_set()
    enter_text_widget.pack(side='bottom', pady=1)
    enter_text_widget.bind('<Return>', on_enter_key_pressed)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (400/2))
    y_cordinate = int((screen_height/2) - (270/2))

    root.geometry(
        "{}x{}+{}+{}".format(400, 270, x_cordinate, y_cordinate))
    # recebendo varias mensagens
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    root.mainloop()

# verifica se o usuario quer fechar a janela do chat


def on_closing_chat():
    if messagebox.askokcancel("Sair", "Deseja sair do chat?"):
        root.destroy()
        clientSocket_ssl.close()
        exit(0)

# verifica se o usuario quer fechar a janela de login


def on_closing():
    if messagebox.askokcancel("Sair", "Deseja sair do login?"):
        login_screen.destroy()
        exit(0)

# verifica se foi apertado a tecla enter


def on_enter_key_login_pressed(event):
    login_verify()

# GUI tela login


def main_account_screen():
    global login_screen, username_verify, username_login_entry
    global password_verify, password_login_entry
    login_screen = Tk()
    # This code helps to disable windows from resizing
    login_screen.resizable(False, False)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.title("Login")
    Label(login_screen, text="Faça o login para usar o chat").pack()
    Label(login_screen, text="").pack()

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(
        login_screen, textvariable=username_verify)
    username_login_entry.pack()
    username_login_entry.focus_set()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(
        login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    password_login_entry.bind('<Return>', on_enter_key_login_pressed)
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10,
           height=1, command=login_verify).pack()

    screen_width = login_screen.winfo_screenwidth()
    screen_height = login_screen.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (300/2))
    y_cordinate = int((screen_height/2) - (210/2))

    login_screen.geometry(
        "{}x{}+{}+{}".format(300, 210, x_cordinate, y_cordinate))

    login_screen.mainloop()


main_account_screen()
