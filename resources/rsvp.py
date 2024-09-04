
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import RSVPModel,EventModel
from schemas import EventSchema, RSVPSchema, RSVPUpdateSchema

blp = Blueprint("rsvps", __name__, description="Operations on rsvps")

@blp.route("/event/<int:event_id>/rsvps")
class Rsvps(MethodView):
    @jwt_required()
    @blp.response(200, RSVPSchema(many=True))
    def get(self, event_id):
        event=EventModel.query.get_or_404(event_id)
        return event.rsvps.all()

@blp.route("/event/<int:event_id>/user/<int:user_id>")
class SendRSVPInvite(MethodView):
    @jwt_required()
    @blp.response(200, RSVPSchema)
    def post(self, event_id, user_id):

        if not RSVPModel.query.filter_by(event_id=event_id, user_id=user_id).first():
            rsvp= RSVPModel(event_id=event_id, user_id=user_id,status="Tentative")

            try:
                db.session.add(rsvp)
                db.session.commit()
            except IntegrityError:
                abort(
                    400,
                    message="An rsvp for that user already exists.",
                )
            except SQLAlchemyError:
                abort(500, message="An error occurred sending the rsvp.")

            return rsvp
        else :
            abort(400, message="An rsvp for that user already exists.")

    @blp.route("/rsvp/<int:rsvp_id>")
    class Rsvp(MethodView):
        @jwt_required()
        @blp.response(200, RSVPSchema)
        def get(self, rsvp_id):
            rsvp = RSVPModel.query.get_or_404(rsvp_id)
            return rsvp

        def delete(self, rsvp_id):
            event = RSVPModel.query.get_or_404(rsvp_id)
            db.session.delete(event)
            db.session.commit()
            return {"message": "Rsvp deleted"}

        @blp.arguments(RSVPUpdateSchema)
        @jwt_required()
        @blp.response(200, RSVPSchema)
        def put(self, rsvp_data, rsvp_id):
            rsvp = RSVPModel.query.get(rsvp_id)

            if rsvp:
                rsvp.status = rsvp_data["status"]
            else:
                rsvp = RSVPModel(id=rsvp_id, **rsvp_data)

            db.session.add(rsvp)
            db.session.commit()

            return rsvp