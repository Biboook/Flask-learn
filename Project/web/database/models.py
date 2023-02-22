from web.flaskapp import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    user_booking = db.relationship("Flights", back_populates="user_flight", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.user_name!r}, login={self.login!r})"


class Flights(db.Model):
    __tablename__ = "flights"
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_from = db.Column(db.String(255))
    flight_to = db.Column(db.String(255))
    start = db.Column(db.String)
    end = db.Column(db.String)
    adults = db.Column(db.Integer)
    child = db.Column(db.Integer)
    identification = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_flight = db.relationship("User", back_populates="user_booking")

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