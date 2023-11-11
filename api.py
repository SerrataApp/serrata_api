from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm import Session

from datetime import timedelta, datetime
from typing import Annotated

from bdtest import fake_users_db
import bdd
import models
import crud
import classes
import schemas
from database import SessionLocal, engine
from get_db import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

database = r"bdd.db"


@app.post("/signup", response_model=schemas.UserData)
def signup_user(user: schemas.UserInDb, db: Session = Depends(get_db)):
    try:
        user: schemas.UserInDb = crud.create_user(db=db, user=user)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le nom d'utilisateur éxiste déjà!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mauvais mot de passe ou nom d'utilisateur",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/score/", response_model=schemas.GameInDb)
def get_game(
        game_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_game(db=db, game_id=game_id)


@app.get("/scores/", response_model=list[schemas.GameInDb])
def get_games(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    games = crud.get_games(db=db, skip=skip, limit=limit)
    return games


@app.get("/users/me/", response_model=schemas.UserData)
async def read_users_me(
        current_user: Annotated[schemas.UserData, Depends(crud.get_current_active_user)]
):
    return current_user


@app.delete("/users/me/", response_model=list[schemas.UserData])
def delete_user(
        user: Annotated[schemas.UserData, Depends(crud.get_current_active_user)],
        db: Session = Depends(get_db)
):
    return crud.delete_user(db=db, id=user.id)


@app.delete("/users/", response_model=schemas.UserData)
def delete_user(
        #TODO: checker si le user est admin
        user: Annotated[schemas.UserData, Depends(crud.get_current_active_user)],
        user_id: int,
        db: Session = Depends(get_db)
):
    if user.admin:
        try:
            user: schemas.UserData = crud.delete_user(db=db, id=user_id)
            return user
        except UnmappedInstanceError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="L'utilisateur n'existe pas!",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour effectuer cette action",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/score/", response_model=schemas.Game)
def create_game(
        #TODO verifier que l'utilisateur est conncté
        game: schemas.Game,
        db: Session = Depends(get_db)
):
    return crud.create_game(game=game, db=db)
