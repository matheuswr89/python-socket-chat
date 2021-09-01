from tkinter import messagebox, Frame, Tk, Label, Button, Entry, Scrollbar, Text, VERTICAL, END
import select
import socket
import threading
import time
import ssl
import re


f = open('caminho-certificado.txt', 'r')
linhas = f.read().split('\n')
CERT_FILE = linhas[0]
KEY_FILE = linhas[1]
f.close()

PORT = 4500
HOST = socket.gethostbyname(socket.gethostname())

entrou = False

class Chat_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.conn = None
        self.addr = None
        self.daemon = True

    def run(self):
        try:
            # Aqui, criamos o nosso mecanismo de Socket para receber a conexão
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Essa linha serve para zerar o TIME_WAIT do Socket
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Esta linha define para qual IP e porta o servidor deve aguardar a conexão
            s.bind((HOST, PORT))
            # Define o limite de conexões
            s.listen(1)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=CERT_FILE,
                                    keyfile=KEY_FILE)
            serverSocket_ssl = context.wrap_socket(s, server_side=True)

            print("Listening for connections on", HOST, ":", PORT)
            # Deixa o Servidor na escuta aguardando as conexões
            self.conn, self.addr = serverSocket_ssl.accept()

            with self.conn:
                print("Connected")
                while self.running:
                    ready, steady, nah = select.select(
                        [self.conn], [self.conn], [])
                    if ready:
                        data = self.conn.recv(4096)
                        data = bytes.decode(data, 'utf-8')
                        if not data:
                            self.conn.send("Server broken".encode("utf-8"))
                            print("Server broken")
                            break
                        chat_transcript_area.insert('end', data+"\n")
                        chat_transcript_area.yview(END)
                time.sleep(0)
            print("Server closed. Type \"exit()\" to quit.")
            self.conn.close()
        except:
            messagebox.showerror(
                "Error", "Não foi possivel iniciar o servidor.")
            guiuser.destroy()
            exit(0)

    def kill(self):
        self.running = False


class Chat_Client(threading.Thread):
    def __init__(self):
        # define as variaveis
        threading.Thread.__init__(self)
        self.host = None
        self.sock = None
        self.sock_ssl = None
        self.running = True

    # inicia a conexao
    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(CERT_FILE)
            self.sock_ssl = context.wrap_socket(
                self.sock, server_hostname=self.host)
            self.sock_ssl.connect((self.host, PORT))
            with self.sock_ssl:
                print("Connected")
                while self.running:
                    ready, steady, nah = select.select(
                        [self.sock_ssl], [self.sock_ssl], [])
                    if ready:
                        self.sock_ssl.send(user.encode('utf-8'))
                        data = self.sock_ssl.recv(4096)
                        data = bytes.decode(data, 'utf-8')
                        if not data:
                            self.sock_ssl.send("Client broken".encode("utf-8"))
                            print("Client broken")
                            break
                        chat_transcript_area.insert('end', data+"\n")
                        chat_transcript_area.yview(END)
                time.sleep(0)
                print("Client closed. Type \"exit()\" to quit.")
        except:
            messagebox.showerror(
                "Error", "Não foi possivel conectar com o servidor.")
            self.conn.close()
            guiuser.destroy()
            exit(0),

    # mata a conexão
    def kill(self):
        self.running = False


class P2PGui(Frame):
    # define algumas variaves e inicia o gui
    def __init__(self):
        self.root = Tk(className="P2P Text Messenger")
        Frame.__init__(self, self.root)

        self.createWidgets()
        self.pack()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (400/2))
        y_cordinate = int((screen_height/2) - (270/2))

        self.root.geometry(
            "{}x{}+{}+{}".format(400, 270, x_cordinate, y_cordinate))
    # cria os componentes da gui

    def createWidgets(self):
        global chat_transcript_area, enter_text_widget
        self.root.bind('<Return>', self.submitText)
        self.root.resizable(False, False)
        self.root.title("Chat")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_chat)
        frame = Frame(self.root)
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
        Label(self.root, text='Enter message:',
              font=("Serif", 12)).pack(side='top')
        enter_text_widget = Text(
            self.root, width=60, height=1, font=("Serif", 12))
        enter_text_widget.focus_set()
        enter_text_widget.pack(side='bottom', pady=1)
        enter_text_widget.bind('<Return>', self.submitText)

    def on_closing_chat(self):
        if messagebox.askokcancel("Sair", "Deseja sair do chat?"):
            self.root.destroy()
            exit(0)

    # envia as mensagens
    def submitText(self, event=None):
        text = enter_text_widget.get(1.0, 'end').strip().encode('utf-8')
        if(text != ''):
            try:
                chat_client.sock_ssl.sendall(user+": "+text)
            except:
                Exception()
            try:
                chat_server.conn.sendall(user+": "+text)
            except:
                Exception()

        if enter_text_widget.get(1.0, 'end').strip() != '':
            text = "Me: " + enter_text_widget.get(1.0, 'end').strip() + "\n"
            chat_transcript_area.insert('end', text)
            chat_transcript_area.yview(END)
            enter_text_widget.delete(1.0, 'end')

    def start(self):
        self.root.mainloop()


def GuiIp():
    global ip_addr, master, iptext
    master = Tk()
    master.resizable(False, False)
    master.protocol("WM_DELETE_WINDOW", on_closing)
    Label(
        master, text="Forneça o IP para se conectar ou\n \"listen\" para iniciar o servidor").grid(row=0)
    iptext = Entry(master)
    iptext.bind('<Return>', on_enter_key_pressed_ip)
    iptext.focus_set()
    iptext.grid(row=1)
    Label(master, text="")
    Button(master, text='Continuar', command=inicia).grid(row=2)
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (180/2))
    y_cordinate = int((screen_height/2) - (90/2))

    master.geometry(
        "{}x{}+{}+{}".format(180, 90, x_cordinate, y_cordinate))

    master.mainloop()


def GuiUser():
    global guiuser, e1
    guiuser = Tk()
    guiuser.resizable(False, False)
    guiuser.protocol("WM_DELETE_WINDOW", on_closing_user)
    Label(
        guiuser, text="Forneça o username:").grid(row=0)
    e1 = Entry(guiuser)
    e1.bind('<Return>', on_enter_key_pressed_user)
    e1.focus_set()
    e1.grid(row=1)
    Label(guiuser, text="")
    Button(guiuser, text='Continuar', command=mostraGUIChat).grid(row=2)
    screen_width = guiuser.winfo_screenwidth()
    screen_height = guiuser.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (120/2))
    y_cordinate = int((screen_height/2) - (90/2))

    guiuser.geometry(
        "{}x{}+{}+{}".format(120, 90, x_cordinate, y_cordinate))

    guiuser.mainloop()


def on_closing():
    if messagebox.askokcancel("Sair", "Deseja sair do chat?"):
        master.destroy()
        exit(0)


def on_closing_user():
    if messagebox.askokcancel("Sair", "Deseja sair do chat?"):
        guiuser.destroy()
        exit(0)


def on_enter_key_pressed_ip(event):
    inicia()


def on_enter_key_pressed_user(event):
    mostraGUIChat()


def inicia():
    global chat_server, chat_client
    ip_re = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    ip_addr = iptext.get()

    chat_server = Chat_Server()
    chat_client = Chat_Client()
    # se o usuario digitar listen, o servidor irá iniciar
    # caso contrario irá tentar se conectar com o IP fornecido
    if ip_addr.rstrip().lower() == 'listen':
        master.destroy()
        chat_server.start()
        GuiUser()
    elif ip_re.match(ip_addr):
        master.destroy()
        chat_client.host = ip_addr.rstrip()
        chat_client.start()
        GuiUser()
    else:
        messagebox.showerror("Error", "Forneça entradas válidas.")


def mostraGUIChat():
    global user, gui
    user = e1.get()
    if(user != ''):
        guiuser.destroy()
        gui = P2PGui()
        gui.start()
    else:
        messagebox.showerror("Error", "Forneça um user válido.")


GuiIp()
