from typing import List, Union
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    playedGames: int
    signupDate: str
    is_active: bool
    wonGames: List['Game'] = []

    class Config:
        orm_mode = True


class UserInDb(User):
    hashed_password: str


class Game(BaseModel):
    id: int
    time: str
    errors: int
    hint: int
    gameDate: str
    playerPseudo: 'User'

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
