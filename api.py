from fastapi import FastAPI, Path, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import bdd
import classes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

database = r"bdd.db"

@app.get("/scores_europe")
def get_scores_europe():
  conn = bdd.create_connection(database)
  scores = bdd.select_scores_europe(conn)
  for i in range(len(scores)):
    scores[i] = classes.to_object_score(scores[i])
  return scores

@app.get("/scores_onu")
def get_scores_onu():
  conn = bdd.create_connection(database)
  scores = bdd.select_scores_onu(conn)
  for i in range(len(scores)):
    scores[i] = classes.to_object_score(scores[i])
  return scores

@app.post("/add_score_europe")
def add_score_europe(score: classes.Score):
  conn = bdd.create_connection(database)
  bdd.create_score_europe(conn, score.temps, score.erreurs, score.joueur)

@app.post("/add_score_onu")
def add_score_onu(score: classes.Score):
  conn = bdd.create_connection(database)
  bdd.create_score_onu(conn, score.temps, score.erreurs, score.joueur)