from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    playedGames = Column(Integer, default=0)
    signupDate = Column(Date)
    is_active = Column(Boolean, default=True)

    wonGames = relationship("Game", back_populates="playerPseudo")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time, index=True)
    errors = Column(Integer)
    hint = Column(Integer)
    gameDate = Column(Date)

    playerPseudo = relationship("User", back_populates="wonGames")
