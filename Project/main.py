from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from fastapi.middleware.wsgi import WSGIMiddleware
from web.main import app

models.Base.metadata.create_all(bind=engine)

fapp = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@fapp.post("/api/users/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.get_user_by_login(db, user_login=user.login)

    if new_user:
        raise HTTPException(status_code=400, detail="Login is already taken by another user. Use another, dattebayo.")
    return crud.create_user(db=db, user=user)


@fapp.post("/api/flight", response_model=schemas.Flight)
def create_flight(user_id:int, flight: schemas.FlightCreate, db: Session=Depends(get_db)):
    return crud.create_flight(user_id=user_id, db=db, flight=flight)


@fapp.get("/api/users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@fapp.get("/api/users/name/{user_name}", response_model=list[schemas.User])
def get_users_by_name(user_name, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user_by_name(db=db, user_name=user_name)
    return users


@fapp.get("/api/users/{login}", response_model=schemas.User)
def get_certain_user(login, db: Session = Depends(get_db)):
    return crud.get_user_by_login(db, login)


@fapp.get("/api/flight", response_model=list[schemas.Flight])
def get_all_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_flights(db)


@fapp.get("/api/user/flights/{user_id}", response_model=list[schemas.Flight])
def get_user_flight(user_id, db: Session = Depends(get_db)):
    return crud.get_user_flights(db, user_id)


fapp.mount("/", WSGIMiddleware(app))

