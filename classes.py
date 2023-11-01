from pydantic import BaseModel
from typing import Union


class Score(BaseModel):
    temps: int
    erreurs: int
    joueur: str


def to_object_score(score):
    objScore = Score(temps=score[0], erreurs=score[1], joueur=score[2])
    return objScore


# Classes relatives à l'authentification

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
