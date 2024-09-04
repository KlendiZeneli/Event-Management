from db import db

class EventTagsModel(db.Model):
    __tablename__ = 'event_tags'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
