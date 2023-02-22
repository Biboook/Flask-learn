from sqlalchemy import Column, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True, nullable=False)
    user_name = Column(String(255))
    password = Column(String(255))

    user_booking = relationship("Flights", back_populates="user_flight", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.user_name!r}, login={self.login!r})"


class Flights(Base):
    __tablename__ = "flights"
    flight_id = Column(Integer, primary_key=True)
    flight_from = Column(String(255))
    flight_to = Column(String(255))
    start = Column(String)
    end = Column(String)
    adults = Column(Integer)
    child = Column(Integer)
    identification = Column(String(255))

    user_id = Column(Integer, ForeignKey("users.user_id"))
    user_flight = relationship("User", back_populates="user_booking")

    def __repr__(self) -> str:
        return f"Flight(flight_id {self.flight_id!r}, flight_from={self.flight_from!r}, flight_to={self.flight_to!r})"


# class Hotels(db.Model):
#     __tablename__ = "hotels"
#     hotel_id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(255))
#     hotel_name = db.Column(db.String(255))
#     start = db.Column(db.String)
#     end = db.Column(db.String)
#     adults = db.Column(db.Integer)
#     child = db.Column(db.Integer)
#
#     def __repr__(self) -> str:
#         return f"Hotel(hotel_id {self.hotel_id!r}, city={self.city!r}, hotel name={self.hotel_name!r})"
#
#
# class Holidays():
#     __tablename__ = "holidays"
#     holidays_id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(255))
#     holiday_name = db.Column(db.String(255))
#     start = db.Column(db.String)
#     end = db.Column(db.String)
#     adults = db.Column(db.Integer)
#     child = db.Column(db.Integer)
#
#
#     def __repr__(self) -> str:
#         return f"Holidays(holidays_id {self.holidays_id!r}, city={self.city!r}, holiday name={self.holiday_name!r})"