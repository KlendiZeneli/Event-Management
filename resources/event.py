from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import EventModel
from schemas import EventSchema, EventUpdateSchema

blp = Blueprint("events", __name__, description="Operations on events")

@blp.route("/event/<int:event_id>")
class Event(MethodView):
    @jwt_required()
    @blp.response(200, EventSchema)
    def get(self, event_id):
        event = EventModel.query.get_or_404(event_id)
        return event

    @jwt_required()
    def delete(self, event_id):
        event = EventModel.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}

    @jwt_required()
    @blp.arguments(EventUpdateSchema)
    def put(self, event_data, event_id):
        event = EventModel.query.get(event_id)

        if event:
            event.name = event_data["name"]
            event.date = event_data["date"]
            event.organiser = event_data["organiser"]
        else:
            event = EventModel(id=event_id, **event_data)

        db.session.add(event)
        db.session.commit()

        return event


@blp.route("/event")
class EventList(MethodView):
    @jwt_required()
    @blp.response(200, EventSchema(many=True))
    def get(self):
        return EventModel.query.all()

    @jwt_required()
    @blp.arguments(EventSchema)
    @blp.response(201, EventSchema)
    def post(self,event_data):
        event = EventModel(**event_data)
        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A event with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the event.")

        return event

