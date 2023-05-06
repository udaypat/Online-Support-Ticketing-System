# import bcrypt, uuid
# from datetime import datetime
# from werkzeug.exceptions import Unauthorized

# from sqlalchemy import desc, func
from flask import current_app as app
from flask import jsonify, request, Markup
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.data.db import db
from app.data.models import Ticket, Comment
from app.data.schema import CommentSchema
from app.utils.validation import Validation, NotFound
from app.utils.auth import Auth, NotAuthorized

# jwt = JWTManager(app)
# salt = bcrypt.gensalt()

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


@app.get("/api/tickets/<ticket_id>/comments")
@jwt_required()
def get_comments(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if ticket:
        comments = (
            db.session.query(Comment)
            .filter(Comment.ticket_id == ticket_id)
            .order_by(Comment.created_at.desc())
            .all()
        )
        return comments_schema.jsonify(comments), 200
    else:
        raise NotFound(status_code=404, msg="Ticket not found")


@app.post("/api/tickets/<ticket_id>/comments")
@jwt_required()
def post_comment(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket:
        current_user_id = get_jwt_identity()
        commentdata = request.get_json()
        body = commentdata["body"]
        Validation.is_valid_string_value(
            body, "Comment Body", alpha_only=False, allow_special_chars=True
        )
        body = Markup(body)

        new_comment = Comment(body=body, ticket_id=ticket_id, user_id=current_user_id)
        db.session.add(new_comment)
        db.session.commit()
        return comment_schema.jsonify(new_comment), 200
    else:
        raise NotFound(status_code=404, msg="Ticket not found")


@app.get("/api/comments/<comment_id>")
@jwt_required()
def get_comment(comment_id):
    comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        return comment_schema.jsonify(comment), 200
    else:
        raise NotFound(status_code=404, msg="Comment not found")


@app.put("/api/comments/<comment_id>")
@jwt_required()
def put_comment(comment_id):
    current_user_id = get_jwt_identity()
    comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        Auth.authorize(current_user_id, comment.user_id)
        commentdata = request.get_json()
        body = commentdata["body"]
        Validation.is_valid_string_value(
            body, "Comment Body", alpha_only=False, allow_special_chars=True
        )
        comment.body = Markup(body)
        db.session.add(comment)
        db.session.commit()
        return comment_schema.jsonify(comment), 200
    else:
        raise NotFound(status_code=404, msg="Comment not found")


@app.delete("/api/comments/<comment_id>")
@jwt_required()
def delete_comment(comment_id):
    current_user_id = get_jwt_identity()
    comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        Auth.authorize(current_user_id, comment.user_id)
        db.session.delete(comment)
        db.session.commit()
        return jsonify("Comment Deleted")
    else:
        raise NotFound(status_code=404, msg="Comment not found")


@app.put("/api/comments/<comment_id>/solution")
@jwt_required()
def mark_comment_as_solution(comment_id):
    current_user_id = get_jwt_identity()
    comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
    ticket = (
        db.session.query(Ticket).filter(Ticket.ticket_id == comment.ticket_id).first()
    )

    is_support = Auth.authorize_support(current_user_id)
    is_admin = Auth.authorize_admin(current_user_id)
    is_owner = Auth.authorize_owner(current_user_id, ticket.student_id)

    if not comment:
        raise NotFound(status_code=404, msg="Comment not found")

    if not ticket:
        raise NotFound(status_code=404, msg="Ticket not found")

    if is_admin or is_support or is_owner:
        if ticket.status == "Open":
            print(is_admin, is_support, is_owner, ticket.status)
            ticket.status = "Resolved"
            comment.solution = 1
            db.session.add(ticket)
            db.session.add(comment)
            db.session.commit()
            print(is_admin, is_support, is_owner, ticket.status)
            return comment_schema.jsonify(comment), 200
        else:
            return jsonify("Ticket already resolved"), 400
    else:
        raise NotAuthorized()


@app.get("/api/test")
def test():
    return jsonify("test api")
