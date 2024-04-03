from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    email= db.Column(db.String(80), unique=True, nullable=False)