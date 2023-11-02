from pydantic import BaseModel
from typing import Union


class Score(BaseModel):
    temps: int
    erreurs: int
    joueur: str


def to_object_score(score):
    objScore = Score(temps=score[0], erreurs=score[1], joueur=score[2])
    return objScore
