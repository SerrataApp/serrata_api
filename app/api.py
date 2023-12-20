from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm import Session

from datetime import timedelta
from typing import Annotated

from . import crud, models, schemas
from .database import engine
from .get_db import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

database = r"bdd.db"


@app.get("/users/me/", response_model=schemas.UserPersonalInfo, tags=["users"])
async def read_users_me(
        current_user: Annotated[schemas.UserData, Depends(crud.get_current_user)]
):
    return current_user


@app.get("/users/", response_model=schemas.UserData, tags=["users"])
async def read_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    user: schemas.UserData = crud.get_user_by_id(db=db, id=user_id)
    return user


@app.delete("/users/me/", response_model=schemas.UserData, tags=["users"])
def delete_user(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        db: Session = Depends(get_db)
):
    return crud.delete_user(db=db, id=user.id)


@app.delete("/users/", response_model=schemas.UserData, tags=["users"])
def delete_user(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        user_id: int,
        db: Session = Depends(get_db)
):
    if user.admin:
        try:
            user: schemas.UserData = crud.delete_user(db=db, id=user_id)
            return user
        except UnmappedInstanceError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="L'utilisateur n'existe pas!",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour effectuer cette action",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.put("/users/me/game", response_model=schemas.UserData, tags=["users"])
def modify_nb_games(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        db: Session = Depends(get_db)
):
    return crud.change_nb_games(db=db, user=user)


@app.post("/signup", response_model=schemas.UserPersonalInfo, tags=["users"])
def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user: schemas.UserInDb = crud.create_user(db=db, user=user)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le nom d'utilisateur éxiste déjà!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token", response_model=schemas.Token, tags=["users"])
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mauvais mot de passe ou nom d'utilisateur",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(crud.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/score/", response_model=schemas.GameInDb, tags=["scores"])
def get_game(
        game_id: int,
        db: Session = Depends(get_db)
):
    try:
        # TODO verifier que l'id de la partie existe
        if game_id < 0:
            raise ResponseValidationError
        return crud.get_game(db=db, game_id=game_id)
    except ResponseValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La partie n'existe pas",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/score/user/", response_model=schemas.UserDataWithGames, tags=["scores"])
def get_games_by_user(
        username: str,
        db: Session = Depends(get_db)
):
    # TODO verifier que l'id de l'utilisateur existe
    try:
        user_data = crud.get_user_by_username(db=db, username=username)
        user_id = user_data.id
        user_games = crud.get_games_by_user(db=db, user_id=user_id)

        user_data_pydantic = schemas.UserData(**user_data.__dict__)

        user_games_pydantic = [schemas.GameInDb(**game.__dict__) for game in user_games]

        user_with_games = schemas.UserDataWithGames(**user_data_pydantic.dict(), games=user_games_pydantic)

        return user_with_games

    except UnmappedInstanceError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'utilisateur n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/score/", response_model=schemas.Game, tags=["scores"])
def create_game(
        user: Annotated[schemas.UserData, Depends(crud.get_current_active_user)],
        game: schemas.Game,
        db: Session = Depends(get_db)
):
    if user.id == game.player_id:
        return crud.create_game(game=game, db=db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour effectuer cette action",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.delete("/score/", response_model=schemas.GameInDb, tags=["scores"])
def delete_game(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        game_id: int,
        db: Session = Depends(get_db)
):
    if user.admin:
        try:
            return crud.delete_game(db=db, game_id=game_id)
        except UnmappedInstanceError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La partie n'existe pas!",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour effectuer cette action",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/scores/", response_model=list[schemas.GameInDb], tags=["scores"])
def get_games(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_games(db=db, skip=skip, limit=limit)


@app.get("/scores/mode/", response_model=list[schemas.GameInDb], tags=["scores"])
def get_games_by_game_mode(
        game_mode_id: int,
        db: Session = Depends(get_db)
):
    games: schemas.GameInDb = crud.get_games_by_game_mode(db=db, game_mode=game_mode_id)
    return games


@app.put("/score/changeState/", response_model=schemas.GameInDb, tags=["scores"])
def modify_game_state(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        game_id: int,
        db: Session = Depends(get_db)
):
    game = crud.get_game(db=db, game_id=game_id)
    if game.player_id == user.id:
        return crud.change_public_state(db=db, game_id=game_id)
    else:
        if user.admin:
            return crud.change_public_state(db=db, game_id=game_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour changer l'état d'une partie!",
            headers={"WWW-Authenticate": "Bearer"},
        )


# DASHBOARD ADMIN

@app.put("/admindisable/", response_model=schemas.UserData, tags=["admin"])
def disable_user(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        user_id: int,
        db: Session = Depends(get_db)
):
    if user.admin:
        selected_user = crud.get_user_by_id(db=db, id=user_id)
        if selected_user is not None:
            return crud.disable_user(db=db, user=selected_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour desactiver un utilisateur!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/adminusers/", response_model=schemas.UserPersonalInfo, tags=["admin"])
def get_user_by_admin(
        user: Annotated[schemas.UserData, Depends(crud.get_current_user)],
        user_id: int,
        db: Session = Depends(get_db)
):
    if user.admin:
        return crud.get_user_by_id(db=db, id=user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas les droits pour récupérer les données d'un utilisateur!",
            headers={"WWW-Authenticate": "Bearer"},
        )
