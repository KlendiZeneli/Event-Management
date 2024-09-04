from db import db

class TagModel(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), unique=False, nullable=False)
    events= db.relationship('EventModel', back_populates='tags',secondary= "event_tags")
