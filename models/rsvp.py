from db import db

class RSVPModel(db.Model):
    __tablename__ = "rsvps"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'),unique= False,nullable=False)
    events= db.relationship('EventModel', back_populates = "rsvps")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('UserModel', back_populates = "rsvps")