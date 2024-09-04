from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TagModel, EventModel
from schemas import TagSchema, EventSchema

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/event/<int:event_id>/tag")
class TagsInEvent(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema(many=True))
    def get(self, store_id):
        event = EventModel.query.get_or_404(store_id)

        return event.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self, tag_data,event_id):

        tag = TagModel(**tag_data,event_id = event_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message= str())

        return tag

@blp.route("/event/<int:event_id>/tag/<int:tag_id>")
class UnlinkTagToEvent(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema)
    def delete(self,event_id,tag_id):
        event = EventModel.query.get_or_404(event_id)
        tag = TagModel.query.get_or_404(tag_id)



        try:
            event.tags.remove(tag)
            db.session.add(event)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(500,message= "An error occurred while removing the tag.")

        return {"message": "Tag successfully removed", "tag": tag}

@blp.route("/tag/<int:tag_id>")
class TagView(MethodView):
        @jwt_required()
        @blp.response(200,TagSchema)
        def get(self, tag_id):
            tag = TagModel.query.get_or_404(tag_id)
            return tag

        @jwt_required()
        @blp.response(
            202,
            description = "Deletes a tag if no event is linked to it.",
            example = {"message": "Tag deleted."}
                      )
        @blp.alt_response(404, description = "Tag not found")
        def delete(self,tag_id):
            tag = TagModel.query.get_or_404(tag_id)

            if not tag.items:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted."}
            abort(400,message = "Could not delete the tag.")
