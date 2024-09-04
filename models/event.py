from db import db

class EventModel(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    organiser = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(), unique=False, nullable=False)
    rsvps = db.relationship('RSVPModel', back_populates ='events', lazy="dynamic",cascade="all, delete, delete-orphan")
    tags = db.relationship('TagModel', back_populates="events", secondary="event_tags")