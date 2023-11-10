import datetime

from sqlalchemy import Boolean, Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    played_games = Column(Integer, default=0)
    signup_date = Column(Date, default=datetime.date.today(), index=True)
    disabled = Column(Boolean, default=False, index=True)
    admin = Column(Boolean, default=False)

    #wonGames = relationship("Game", backref="user")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    game_mode = Column(Integer, index=True)
    time = Column(Time, index=True)
    errors = Column(Integer, index=True)
    hint = Column(Integer, index=True)
    game_date = Column(Date, default=datetime.date.today(), index=True)
    player_id = Column(Integer, ForeignKey("users.id"))
