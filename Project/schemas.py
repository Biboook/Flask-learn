from pydantic import BaseModel


class FlightBase(BaseModel):
    flight_from: str
    flight_to: str
    start: str
    end: str
    adults: int
    child: int

    
class FlightCreate(FlightBase):
    pass


class Flight(FlightBase):
    flight_id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str
    user_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    user_booking: list[Flight] = []

    class Config:
        orm_mode = True
