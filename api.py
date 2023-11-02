from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta
from typing import Annotated

from bdtest import fake_users_db
import bdd
import models
import crud
import classes
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

#TODO: A refaire
# @app.post("/signup", response_model=schemas.UserInDb)
# async def signup_user(
#         username: str,
#         password: str,
#         email: str,
#         fullname: str,
# ):
#     # TODO: check if the password is strong enough
#     if username in fake_users_db:
#         raise HTTPException(
#             status_code=400,
#             detail="Ce nom d'utlisateur est déjà pris",
#         )
#     fake_users_db[username] = {
#         "username": username,
#         "full_name": fullname,
#         "email": email,
#         "hashed_password": crud.get_password_hash(password),
#         "disabled": False,
#     }
#     return {"username": fake_users_db[username]}
#
# #TODO: A refaire
# @app.delete("/users/me")
# async def delete_user(current_user: Annotated[schemas.User, Depends(crud.get_current_active_user)]):
#     del fake_users_db[current_user.username]
#     return {"message": "User deleted successfully"}
#

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# #TODO: A refaire
# @app.get("/users/me/", response_model=schemas.User)
# async def read_users_me(
#         current_user: Annotated[schemas.User, Depends(crud.get_current_active_user)]
# ):
#     return current_user
#
# #TODO: A refaire
# @app.get("/users/me/items/")
# async def read_own_items(
#         current_user: Annotated[schemas.User, Depends(crud.get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
#
# #TODO: A refaire
# @app.post("/test/")
# async def test(message: str):
#     return {"message": message}
