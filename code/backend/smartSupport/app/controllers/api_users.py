import bcrypt
import uuid

# from datetime import datetime

from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)


from app.data.db import db
from app.data.models import User, Role, Tag
from app.data.schema import UserSchema
from app.utils.validation import *
from app.utils.auth import Auth, NotAuthorized

jwt = JWTManager(app)
salt = bcrypt.gensalt()


# Create User
@app.post("/api/user/register")
def register():
    # Getting data
    userdata = request.get_json()
    usr = User.query.filter_by(username=userdata["username"]).first()
    em = User.query.filter_by(email=userdata["email"]).first()
    student_role = Role.query.filter(Role.name == "Student").first()

    if usr or em:
        return jsonify("User already Exists"), 409
    password = userdata["password"].encode("utf-8")

    # Hashing Password
    hashed_pass = bcrypt.hashpw(password, salt)

    fs_uniquifier = uuid.uuid4().hex

    new_user = User(
        username=userdata["username"],
        email=userdata["email"],
        password=hashed_pass,
        first_name=userdata["first_name"],
        last_name=userdata["last_name"],
        fs_uniquifier=fs_uniquifier,
    )

    new_user.roles.append(student_role)
    # commiting Data
    db.session.add(new_user)
    db.session.commit()
    user_schema = UserSchema()
    return user_schema.jsonify(new_user)


# User Login
@app.post("/api/user/login")
def login():
    # Getting user Creds
    userdata = request.get_json()
    user_name = userdata["username"]
    password = userdata["password"].encode("utf-8")

    # Getting Creds from db
    curr_user = User.query.filter_by(username=user_name).first()

    # checking creds
    if curr_user is None:
        return jsonify({"msg": "Bad username"})
    elif bcrypt.checkpw(password, curr_user.password):
        # Creating JWT token
        access_token = create_access_token(identity=curr_user.user_id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad password"})


# get all users
@app.get("/api/user/all")
def get_users():
    user_list = User.query.order_by(User.user_id).all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(user_list)
    return jsonify(output)


# get admin and support users
@app.get("/api/user/admin-and-support")
def get_admin__and_support_users():
    user_list = User.query.join(User.roles).filter(Role.name.in_(['Admin', 'Support'])).all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(user_list)
    return jsonify(output)


# Get a single user by JWT token
@app.get("/api/user")
@jwt_required()
def get_user():
    current_userid = get_jwt_identity()

    usr = User.query.filter_by(user_id=current_userid).first()

    # Converts Sql obeject to json object
    user_schema = UserSchema()
    output = user_schema.dump(usr)
    return jsonify(output)


# Update a user
@app.put("/api/user")
@jwt_required()
def update_user():
    current_userid = get_jwt_identity()

    usr = User.query.filter_by(user_id=current_userid).first()

    user_data = request.get_json()
    # usr.username = user_data["username"]
    # usr.password = user_data["password"]
    usr.email = user_data["email"]
    usr.first_name = user_data["first_name"]
    usr.last_name = user_data["last_name"]

    db.session.commit()

    return jsonify(user_data)


# Delete a user
@app.delete("/api/user")
@jwt_required()
def delete_tracker():
    current_userid = get_jwt_identity()

    User.query.filter_by(user_id=current_userid).delete()
    db.session.commit()

    return jsonify("User deleted successfully")


# Assign tags to a user


# Change tags for a user


# Assign role to a user
@app.put("/api/user/roles")
@jwt_required()
def add_role():
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()
    userdata = request.json
    username = userdata["username"]
    roles = userdata["roles"]

    user = User.query.filter(User.username == userdata["username"]).first()
    if not user:
        raise NotFound(status_code=404, msg="User not found")

    found_roles = Role.query.filter(Role.name.in_(roles)).all()
    if len(found_roles) != len(roles):
        not_found_roles = set(roles) - set([role.name for role in found_roles])
        raise NotFound(status_code=404, msg=f"Roles not found: {not_found_roles}")
    # print(user.roles)
    # for role in found_roles:
    #     if role not in user.roles:
    #         print("appended", role)
    #         user.roles.append(role)
    #     elif role in user.roles:
    #         print("removed", role)

    #         user.roles.remove(role)

    # db.session.add(user)
    user.roles = found_roles
    db.session.commit()
    user_schema = UserSchema()

    return user_schema.jsonify(user)


# remove roles from a user
@app.delete("/api/user/roles")
@jwt_required()
def delete_role():
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    userdata = request.get_json()
    user = User.query.filter(User.username == userdata["username"]).first()
    role = Role.query.filter(Role.name == userdata["role"]).first()

    if not user:
        raise NotFound(status_code=404, msg="User not found")
    if not role:
        raise NotFound(status_code=404, msg="Role not found")

    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return jsonify("Role removed successfully"), 204
    else:
        return jsonify("Role doesn't exist for user"), 400


# Assign a tag to a user
@app.post("/api/user/tags")
@jwt_required()
def add_usertag():
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    userdata = request.get_json()
    user = User.query.filter(User.username == userdata["username"]).first()
    tag = Tag.query.filter(Tag.tag_id == userdata["tag_id"]).first()
    if not user:
        raise NotFound(status_code=404, msg="User not found")
    if not tag:
        raise NotFound(status_code=404, msg="Tag not found")

    if tag not in user.tags:
        user.tags.append(tag)
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        return user_schema.jsonify(user)
    else:
        return jsonify("Tag already exists for the user"), 400


# Remove a tag from a user
@app.put("/api/user/tags")
@jwt_required()
def remove_usertag():
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    userdata = request.get_json()
    user = User.query.filter(User.username == userdata["username"]).first()
    tag = Tag.query.filter(Tag.tag_id == userdata["tag_id"]).first()
    if not user:
        raise NotFound(status_code=404, msg="User not found")
    if not tag:
        raise NotFound(status_code=404, msg="Tag not found")

    if tag in user.tags:
        user.tags.remove(tag)
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        return user_schema.jsonify(user)
    else:
        return jsonify("Tag doesn't exist for the user"), 400
