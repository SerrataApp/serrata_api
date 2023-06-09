import sqlite3
from sqlite3 import Error

def create_connection(db_file):
  """Créer une connexion à un fichier de base de données"""
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
  except Error as e:
    print(e)
  return conn
  
def create_table(conn, create_table_sql):
  """Créer une table depuis la requête SQL donnée"""
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)

def main():
  database = r"bdd.db"
  conn = create_connection(database)
  if conn is not None:
    continue
  else:
    print("Error, can't create the database connection")

if __name__ == '__main__':
  main()