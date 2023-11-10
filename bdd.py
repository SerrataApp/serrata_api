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


def create_score(conn, table, temps, erreurs, joueur):
    sql = f"SELECT MAX(idScore) FROM {table};"
    cur = conn.cursor()
    cur.execute(sql)
    idMax = cur.fetchall()[0][0]
    data = (temps, erreurs, joueur)
    if (idMax == None):
        sql = f"INSERT INTO {table} (idScore, temps, erreurs, joueur) VALUES (1, ?, ?, ?)"
    else:
        sql = f"INSERT INTO {table} (idScore, temps, erreurs, joueur) VALUES (?, ?, ?, ?)"
        data = (idMax + 1,) + data
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


def select_scores(conn, table):
    sql = f"SELECT temps, erreurs, joueur FROM {table} ORDER BY temps;"
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()
    return row


def main():
    database = r"bdd.db"

    sql_create_scores_table = """
    CREATE TABLE IF NOT EXISTS Scores (
    idScore INT PRIMARY KEY,
    idJoueur INT,
    temps INT,
    erreurs INT,
    indices INT,
    datePartie DATE,
    FOREIGN KEY (idJoueur) REFERENCES Utilisateur(idUtilisateur)
    );"""

    sql_create_scores_europe_table = """
    CREATE TABLE IF NOT EXISTS ScoresEurope (
    idScore INT PRIMARY KEY,
    temps INT,
    erreurs INT,
    joueur VARCHAR
    );"""

    sql_create_scores_afrique_table = """
    CREATE TABLE IF NOT EXISTS ScoresAfrique (
    idScore INT PRIMARY KEY,
    temps INT,
    erreurs INT,
    joueur VARCHAR
    );"""

    sql_create_scores_asie_table = """
    CREATE TABLE IF NOT EXISTS ScoresAsie (
      idScore INT PRIMARY KEY,
      temps INT,
      erreurs INT,
      joueur VARCHAR
    );"""

    sql_create_scores_monde_table = """
    CREATE TABLE IF NOT EXISTS ScoresMonde (
      idScore INT PRIMARY KEY,
      temps INT,
      erreurs INT,
      joueur VARCHAR
    );"""

    slq_create_utilisateur_table = """
    CREATE TABLE IF NOT EXISTS Utilisateur (
    idUtilisateur INT PRIMARY KEY,
    pseudo VARCHAR,
    password VARCHAR,
    email VARCHAR,
    nbPartiesLance INT
    dateInscription DATE
    );"""

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, slq_create_utilisateur_table)
        create_table(conn, sql_create_scores_europe_table)
        create_table(conn, sql_create_scores_afrique_table)
        create_table(conn, sql_create_scores_monde_table)
    else:
        print("Error, can't create the database connection")

if __name__ == '__main__':
    main()
