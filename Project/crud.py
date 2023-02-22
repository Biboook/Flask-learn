from sqlalchemy.orm import Session
import models, schemas


def get_user_by_login(db: Session, user_login: int)->Session.query:
    return db.query(models.User).filter(models.User.login == user_login).first()


def get_user_by_name(db: Session, user_name: str)->Session.query:
    return db.query(models.User).filter(models.User.user_name == user_name).all()


def get_all_users(db: Session, skip: int = 0, limit: int = 100)->Session.query:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_identification_by_id(db: Session, flight_id: int)->Session.query:
    return db.query(models.User).filter(models.User.flight_id == flight_id).first()


def get_user_flights(db: Session, user_id: int)->Session.query:
    return db.query(models.Flights).filter(models.Flights.user_id == user_id).all()


def get_all_flights(db: Session, flight_id: str, skip: int = 0, limit: int = 100) -> Session.query:
    return db.query(models.Flights).filter(models.Flights.flight_id == flight_id).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate)->models.User:
    new_user = models.User(login=user.login, 
                            user_name=user.user_name,
                            password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_flight(db: Session, car: schemas.FlightCreate, user_id)->models.Flights:
    new_car = models.Flights(**car.dict(), user_id=user_id)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car



