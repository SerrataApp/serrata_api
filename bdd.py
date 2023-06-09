import sqlite3
from sqlite3 import Error

def create_connection(db_file):
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
  except Error as e:
    print(e)
  return conn
  
def create_table(conn, create_table_sql):
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)

def create_score_europe(conn, temps, erreurs, joueur):
  sql = "SELECT MAX(idScore) FROM ScoresEurope;"
  cur = conn.cursor()
  cur.execute(sql)
  idMax = cur.fetchall()[0][0]
  data = (temps, erreurs, joueur)
  if(idMax == None):
    sql = "INSERT INTO ScoresEurope (idScore, temps, erreurs, joueur) VALUES (1, ?, ?, ?)"
  else:
    sql = "INSERT INTO ScoresEurope (idScore, temps, erreurs, joueur) VALUES (?, ?, ?, ?)"
    data = (idMax + 1,) + data
  cur = conn.cursor()
  cur.execute(sql, data)
  conn.commit()
  return cur.lastrowid

def create_score_onu(conn, temps, erreurs, joueur):
  sql = "SELECT MAX(idScore) FROM ScoresOnu;"
  cur = conn.cursor()
  cur.execute(sql)
  idMax = cur.fetchall()[0][0]
  data = (temps, erreurs, joueur)
  if(idMax == None):
    sql = "INSERT INTO ScoresOnu (idScore, temps, erreurs, joueur) VALUES (1, ?, ?, ?)"
  else:
    sql = "INSERT INTO ScoresOnu (idScore, temps, erreurs, joueur) VALUES (?, ?, ?, ?)"
    data = (idMax + 1,) + data
  cur = conn.cursor()
  cur.execute(sql, data)
  conn.commit()
  return cur.lastrowid

def select_scores_europe(conn):
  sql = "SELECT temps, erreurs, joueur FROM ScoresEurope ORDER BY temps;"
  cur = conn.cursor()
  cur.execute(sql)
  row = cur.fetchall()
  return row

def select_scores_onu(conn):
  sql = "SELECT temps, erreurs, joueur FROM ScoresOnu ORDER BY temps;"
  cur = conn.cursor()
  cur.execute(sql)
  row = cur.fetchall()
  return row

def main():
  database = r"bdd.db"

  sql_create_scores_europe_table = """
  CREATE TABLE IF NOT EXISTS ScoresEurope (
    idScore INT PRIMARY KEY,
    temps INT,
    erreurs INT,
    joueur VARCHAR
  );"""

  sql_create_scores_onu_table = """
  CREATE TABLE IF NOT EXISTS ScoresOnu (
    idScore INT PRIMARY KEY,
    temps INT,
    erreurs INT,
    joueur VARCHAR
  );"""

  conn = create_connection(database)
  if conn is not None:
    create_table(conn, sql_create_scores_europe_table)
    create_table(conn, sql_create_scores_onu_table)
  else:
    print("Error, can't create the database connection")

if __name__ == '__main__':
  main()