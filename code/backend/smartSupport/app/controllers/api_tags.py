from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.data.db import db
from app.data.models import Tag
from app.data.schema import TagSchema
from app.utils.auth import Auth, NotAuthorized


# Get all tags
@app.get("/api/tags")
@jwt_required()
def get_all_tags():
    tag_lists = Tag.query.order_by(Tag.tag_id).all()

    tag_schema = TagSchema(many=True)
    output = tag_schema.dump(tag_lists)

    return jsonify(output)


# Add a new tag
@app.post("/api/tags")
@jwt_required()
def create_tag():
    current_user_id = get_jwt_identity()
    print("Sacac")
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    tag_data = request.get_json()
    tag = Tag.query.filter(Tag.name == tag_data["name"]).first()

    if not tag:
        db.session.add(Tag(name=tag_data["name"]))
        db.session.commit()
        new_tag = Tag.query.filter_by(name=tag_data["name"]).first()
        return jsonify(f"Tag created successfully with id {new_tag.tag_id}")
    else:
        return jsonify("Tag with given name already exists"), 400


# Change name of a tag
@app.put("/api/tags/<tag_id>")
@jwt_required()
def edit_tag(tag_id):
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    tag_data = request.get_json()
    tag = Tag.query.filter(Tag.tag_id == tag_id).first()

    if tag:
        tag.name = tag_data["name"]
        db.session.add(tag)
        db.session.commit()

        tag_schema = TagSchema()
        output = tag_schema.dump(tag)
        return jsonify(output)
    else:
        return jsonify("Tag doesn't exist"), 400


# Change name of a tag
@app.delete("/api/tags/<tag_id>")
@jwt_required()
def delete_tag(tag_id):
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    tag = Tag.query.filter(Tag.tag_id == tag_id).first()

    if tag:
        db.session.delete(tag)
        db.session.commit()
        return jsonify(f"Tag name delted"), 204
    else:
        return jsonify("Tag doesn't exist"), 400
