from typing import Union
from pydantic import BaseModel

import schemas


class User(BaseModel):
    id: int
    pseudo: str
    email: str
    playedGames: int
    signupDate: str
    is_active: bool
    wonGames: list[schemas.Game] = []

    class Config:
        orm_mode = True


class UserCreate(User):
    hashed_password: str


class Game(BaseModel):
    id: int
    time: str
    errors: int
    hint: int
    gameDate: str
    playerPseudo: User

    class Config:
        orm_mode = True