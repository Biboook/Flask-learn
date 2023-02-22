from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:/Users/77471/PycharmProjects/final/Project/database.db'

# # Adding PostgreSQL database URI to a config
# # pip install psycopg2
# app.config['SQLALCHEMY_DATABASE_URI'] = r"postgresql://postgres:123@localhost:5432/db"

with app.app_context():
    db.init_app(app)

app.config['SECRET_KEY'] = "biba"

