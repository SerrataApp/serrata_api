from sqlalchemy import update
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from dotenv import load_dotenv
import os
from numpy import invert

from app.get_db import get_db
from app import models, schemas

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_JWT")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SEL = os.getenv("SEL")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO reorganiser ce fichier en mode CRUD


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + SEL, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password + SEL)


def get_user_by_username(db: Session, username: str):
    user: schemas.UserData = db.query(models.User).filter(models.User.username == username).first()
    return user


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_game_public_state(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first().public


def get_games(db: Session, skip: int, limit: int):
    return db.query(models.Game).offset(skip).limit(limit).all()


def get_games_by_user(db: Session, user_id: int):
    return db.query(models.Game).filter(models.Game.player_id == user_id).all()


def get_games_by_game_mode(db: Session, game_mode: int):
    return db.query(models.Game).filter(models.Game.game_mode == game_mode, models.Game.public).all()
  
  
def update_game(db: Session, game_id: int, data: dict):
    db.execute(update(models.Game).where(models.Game.id == game_id).values(data))
    db.commit()
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def update_user(db: Session, user_id: int, data: dict):
    db.execute(update(models.User).where(models.User.id == user_id).values(data))
    db.commit()
    return db.query(models.User).filter(models.User.id == user_id).first()
  

def create_user(db: Session, user: schemas.UserInDb):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        signup_date=datetime.today().date()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_game(db: Session, game: schemas.Game):
    user: schemas.UserData = get_user_by_id(db=db, id=game.player_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utilisateur n'existe pas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_game = models.Game(
        game_mode=game.game_mode,
        time=game.time,
        errors=game.errors,
        hint=game.hint,
        game_date=datetime.today().date(),
        player_id=game.player_id,
        public=game.public,
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return game


def delete_game(db: Session, game_id: int):
    db_game: schemas.GameInDb = get_game(db=db, game_id=game_id)
    db.delete(db_game)
    db.commit()
    return db_game


def delete_user(db: Session, id: int):
    db_user = get_user_by_id(db=db, id=id)
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.UserData, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def change_public_state(db: Session, game_id: int):
    state: bool = get_game_public_state(db=db, game_id=game_id)
    state = invert(state)
    data = {"public": state}
    return update_game(db=db, game_id=game_id, data=data)


def change_nb_games(db: Session, user: schemas.UserData):
    nb_games: int = user.played_games
    nb_games += 1
    data = {"played_games": nb_games}
    return update_user(db=db, user_id=user.id, data=data)
