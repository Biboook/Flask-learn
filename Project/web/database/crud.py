from .models import User, db, Flights


def add_user(user:User)->None:
    db.session.add(user)
    db.session.commit()


def delete_user(user:User)->None:
    db.session.delete(user)
    db.session.commit()


def get_all_users()->db.Query:
    return User.query.all()


def add_flight(flight:Flights)->None:
    db.session.add(flight)
    db.session.commit()

