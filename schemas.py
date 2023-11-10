import datetime
from typing import List, Union
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str

    #wonGames: List['Game'] = []

    class Config:
        orm_mode = True

class UserData(User):
    id: int
    played_games: int
    signup_date: datetime.date
    disabled: bool


class UserInDb(User):
    hashed_password: str


class Game(BaseModel):
    id: int
    time: str
    errors: int
    hint: int
    gameDate: str
    player_pseudo: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
