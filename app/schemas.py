import datetime
from typing import List, Union, Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    signup_date: datetime.date

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserData(User):
    id: int
    played_games: int


class UserPersonalInfo(UserData):
    email: str
    signup_date: datetime.date
    disabled: bool
    admin: bool
    cgu: bool


class UserInDb(UserPersonalInfo):
    password: str


class Game(BaseModel):
    game_mode: int
    time: int
    errors: int
    hint: int
    game_date: datetime.date
    player_id: int
    public: bool

    class Config:
        orm_mode = True


class GameInDb(Game):
    id: Optional[int]
    game_date: Optional[datetime.date]


class UserDataWithGames(UserData):
    games: List[GameInDb] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
