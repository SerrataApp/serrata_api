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
    scores = bdd.select_scores(conn, "ScoresEurope")
    for i in range(len(scores)):
        scores[i] = classes.to_object_score(scores[i])
    return scores


@app.get("/scores_afrique")
def get_scores_afrique():
    conn = bdd.create_connection(database)
    scores = bdd.select_scores(conn, "ScoresAfrique")
    for i in range(len(scores)):
        scores[i] = classes.to_object_score(scores[i])
    return scores


@app.get("/scores_monde")
def get_scores_monde():
    conn = bdd.create_connection(database)
    scores = bdd.select_scores(conn, "ScoresMonde")
    for i in range(len(scores)):
        scores[i] = classes.to_object_score(scores[i])
    return scores


@app.post("/add_score_europe")
def add_score_europe(score: classes.Score):
    conn = bdd.create_connection(database)
    bdd.create_score(conn, "ScoresEurope", score.temps, score.erreurs, score.joueur)


@app.post("/add_score_afrique")
def add_score_afrique(score: classes.Score):
    conn = bdd.create_connection(database)
    bdd.create_score(conn, "ScoresAfrique", score.temps, score.erreurs, score.joueur)


@app.post("/add_score_monde")
def add_score_monde(score: classes.Score):
    conn = bdd.create_connection(database)
    bdd.create_score(conn, "ScoresMonde", score.temps, score.erreurs, score.joueur)
