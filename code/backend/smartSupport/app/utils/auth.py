import json, re
from werkzeug.exceptions import HTTPException
from flask import make_response

from app.data.models import User, Role
from app.data.db import db


class NotAuthorized(HTTPException):
    def __init__(self):
        self.response = make_response(
            json.dumps('You are Not Authorized to perform this action'), 401)


class Auth():
    def authorize(current_user_id, resource_owner_id):
        if str(current_user_id) != str(resource_owner_id):
            raise NotAuthorized()

    def authorize_owner(current_user_id, resource_owner_id):
        return str(current_user_id) == str(resource_owner_id)

    def authorize_support(current_user_id):
        current_user = db.session.query(User).filter(User.user_id==current_user_id).first()
        support_role = Role.query.filter(Role.name == "Support").first()
        return support_role in current_user.roles

    def authorize_admin(current_user_id):
        current_user = db.session.query(User).filter(User.user_id==current_user_id).first()
        admin_role = Role.query.filter(Role.name == "Admin").first()
        return admin_role in current_user.roles