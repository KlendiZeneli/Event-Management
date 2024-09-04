from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(), unique=False, nullable=True)
    password = db.Column(db.String(), nullable=False)
    rsvps = db.relationship('RSVPModel', back_populates='user')