import sqlite3,sys

def criarTabelas():
  try:
      sqliteConnection = sqlite3.connect('database.db')
      tableMensagem = '''CREATE TABLE mensagens(
                                  mensagem TEXT NOT NULL,
                                  idUsuario INTEGER);'''
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
      print("Error while creating a sqlite table", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()
################################################################
def insertMensagem(mensagem, idUsuario):
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()
      query = """INSERT INTO mensagens(mensagem ,idUsuario)  VALUES  (?, ?)"""
      count = cursor.execute(query,(mensagem, idUsuario))
      sqliteConnection.commit()
      cursor.close()
  except sqlite3.Error as error:
      exc_type, exc_value, exc_tb = sys.exc_info()
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
      exc_type, exc_value, exc_tb = sys.exc_info()
  finally:
      if (sqliteConnection):
          sqliteConnection.close()
################################################################
def getUsuario(email, senha):
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()

      query = """select id from user where email = ? and senha= ?"""
      cursor.execute(query, (email,senha))
      records = cursor.fetchall()
      cursor.close()
      return records
  except sqlite3.Error as error:
      print("Failed to read data from sqlite table", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()
################################################################
def getUsuarioName(id):
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()

      query = """select email from user where id = ?"""
      cursor.execute(query, (id,))
      records = cursor.fetchall()
      cursor.close()
      return records
  except sqlite3.Error as error:
      print("Failed to read data from sqlite table", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()
################################################################
def getMensagens():
  try:
      sqliteConnection = sqlite3.connect('database.db')
      cursor = sqliteConnection.cursor()

      query = """SELECT * from mensagens"""
      cursor.execute(query)
      records = cursor.fetchall()
      for row in records:
          retorno = getUsuarioName(int(row[1]))[0][0]
          print('{}: {}'.format(retorno,row[0]))
      cursor.close()

  except sqlite3.Error as error:
      print("Failed to read data from sqlite table", error)
  finally:
      if sqliteConnection:
          sqliteConnection.close()