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

def create_score_europe(conn, score, joueur):
  sql = "SELECT MAX(id) FROM ScoresEurope;"
  cur = conn.cursor()
  cur.execute(sql)
  idMax = cur.fetchall()[0][0]
  if(idMax == None):
    sql = "INSERT INTO ScoresEurope (idScore, temps, joueur) VALUES (1, ?, ?)"
  else:
    sql = "INSERT INTO ScoresEurope (idScore, temps, joueur) VALUES (?, ?, ?)"
    data = (idMax + 1, score, joueur)
  cur = conn.cursor()
  cur.execute(sql, data)
  conn.commit()
  return cur.lastrowid

def create_score_onu(conn, score, joueur):
  sql = "SELECT MAX(id) FROM ScoresEurope;"
  cur = conn.cursor()
  cur.execute(sql)
  idMax = cur.fetchall()[0][0]
  if(idMax == None):
    sql = "INSERT INTO ScoresOnu (idScore, temps, joueur) VALUES (1, ?, ?)"
  else:
    sql = "INSERT INTO ScoresOnu (idScore, temps, joueur) VALUES (?, ?, ?)"
    data = (idMax + 1, score, joueur)
  cur = conn.cursor()
  cur.execute(sql, data)
  conn.commit()
  return cur.lastrowid

def main():
  database = r"bdd.db"

  sql_create_scores_europe_table = """
  CREATE TABLE IF NOT EXISTS ScoresEurope (
    idScore INT PRIMARY KEY,
    temps INT,
    joueur VARCHAR
  );"""

  sql_create_scores_onu_table = """
  CREATE TABLE IF NOT EXISTS ScoresOnu (
    idScore INT PRIMARY KEY,
    temps INT,
    joueur VARCHAR
  );"""

  conn = create_connection(database)
  if conn is not None:
    create_table(conn, sql_create_scores_europe_table)
  else:
    print("Error, can't create the database connection")

if __name__ == '__main__':
  main()