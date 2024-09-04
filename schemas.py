from enum import Enum

from marshmallow import Schema,fields

class PlainEventSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    date=fields.Str(required=True)
    organiser=fields.Str(required=True)

class PlainTagSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)

class PlainRSVPSchema(Schema):
    id=fields.Int(dump_only=True)
    status= fields.Str(required=True)

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)

class UserRegisterSchema(UserSchema):
    email=fields.Str(required=True)

class RSVPSchema(PlainRSVPSchema):
    user_id= fields.Int(dump_only=True)
    user=fields.Nested(UserSchema(),dump_only=True)
    event_id=fields.Int(load_only=True)
    event=fields.Nested(PlainEventSchema(), dump_only=True)

class EventSchema(PlainEventSchema):
        RSVPs = fields.List(fields.Nested(PlainRSVPSchema()), dump_only=True)
        tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    event_id=fields.Int(load_only=True)
    event=fields.List(fields.Nested(PlainEventSchema(), dump_only=True))

class RSVPUpdateSchema(Schema):
    status=fields.Str(load_only=True)

class EventUpdateSchema(Schema):
    name = fields.Str(load_only=True)
    date = fields.Str(load_only=True)
    organiser = fields.Str(load_only=True)

