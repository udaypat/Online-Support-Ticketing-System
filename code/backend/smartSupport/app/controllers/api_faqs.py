from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.data.db import db
from app.data.models import Faqs
from app.data.schema import FaqsSchema

from app.utils.validation import *
from app.utils.auth import Auth, NotAuthorized


# Get all faqs
@app.get("/api/faqs")
@jwt_required()
def get_faqs():
    faq_list = db.session.query(Faqs).all()

    faq_schema = FaqsSchema(many=True)
    output = faq_schema.dump(faq_list)
    return jsonify(output)


# get faq by id
@app.get("/api/faqs/<faq_id>")
@jwt_required()
def faq_byID(faq_id):
    faq = db.session.query(Faqs).filter_by(faq_id=faq_id).first()
    faq_schema = FaqsSchema()
    output = faq_schema.dump(faq)
    return jsonify(output)


# Create new Faq
@app.post("/api/faqs")
@jwt_required()
def create_faq():
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    faq_data = request.get_json()

    db.session.add(Faqs(query=faq_data["question"], answer=faq_data["answer"]))
    db.session.commit()
    faq = db.session.query(Faqs).filter_by(query=faq_data["question"]).first()

    return jsonify(f"Faq created successfully with id {faq.faq_id}")


# update a faq
@app.put("/api/faqs/<faq_id>")
@jwt_required()
def update_faq(faq_id):
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    faq = db.session.query(Faqs).filter_by(faq_id=faq_id).first()
    if faq is None:
        return jsonify("No log found")
    else:
        faq_data = request.get_json()
        faq.query = faq_data["question"]
        faq.answer = faq_data["answer"]
        db.session.commit()
        return jsonify(faq=faq_data, msg="Faq updated Successfully")


# Delete a faq
@app.delete("/api/faqs/<faq_id>")
@jwt_required()
def delete_faq(faq_id):
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    db.session.query(Faqs).filter_by(faq_id=faq_id).delete()
    db.session.commit()
    return jsonify(f"Faq delete with id {faq_id} successfully")
