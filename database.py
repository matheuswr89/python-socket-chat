import sqlite3

def criarTabelas():
  try:
      sqliteConnection = sqlite3.connect('database.db')
      tableMensagem = '''CREATE TABLE mensagens(
                        id INTEGER PRIMARY KEY,
                        mensagem TEXT NOT NULL);'''
      tableUser = '''CREATE TABLE user (
                                  id INTEGER PRIMARY KEY,
                                  email TEXT NOT NULL,
                                  senha TEXT NOT NULL);'''

      cursor = sqliteConnection.cursor()
      cursor.execute(tableUser)
      sqliteConnection.commit()
      cursor.execute(tableMensagem)
      sqliteConnection.commit()
      cursor.close()
  except sqlite3.Error as error:
      print("Erro ao criar a tabela, ela já existe.", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()
################################################################
def insertMensagem(mensagem):
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()
      query = """INSERT INTO mensagens(mensagem) VALUES (?)"""
      cursor.execute(query,(mensagem.decode('utf-8'),))
      sqliteConnection.commit()
      cursor.close()
  except sqlite3.Error as error:
      print("Erro ao inserir os dados em mensagens.", error)
  finally:
      if (sqliteConnection):
          sqliteConnection.close()
################################################################
def insertUsuario(email, senha):
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()
      query = """INSERT INTO user(email, senha)  VALUES  (?, ?)"""
      usuario = (email, senha)
      cursor.execute(query,usuario)
      sqliteConnection.commit()
      cursor.close()
  except sqlite3.Error as error:
      print("Erro ao inserir os dados em user.", error)
  finally:
      if (sqliteConnection):
          sqliteConnection.close()
################################################################
def getUsuarioName(email):
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()

      query = """select senha from user where email = ?"""
      cursor.execute(query, (email,))
      records = cursor.fetchone()
      cursor.close()
      return records
  except sqlite3.Error as error:
      print("Erro ao ler os dados da tabela", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()
################################################################
def getMensagens():
  try:
      mensagens = ''
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()
      query = """SELECT mensagem from mensagens"""
      cursor.execute(query)
      records = cursor.fetchall()
      for row in records:
          mensagens+= str(row[0])
      cursor.close()
      return mensagens
  except sqlite3.Error as error:
      print("Erro ao ler os dados da tabela", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()