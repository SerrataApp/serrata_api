from pydantic import BaseModel

class Score(BaseModel):
  temps: int
  joueur: str

def to_object_score(score):
  objScore = Score(temps=score[0], joueur=score[1])
  return objScore