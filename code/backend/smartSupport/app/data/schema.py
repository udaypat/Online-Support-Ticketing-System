from flask import current_app as app

# from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.data.models import Faqs, Tag, Role

ma = Marshmallow(app)


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # fileds = ("role_id", "name")
        model = Role


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "email", "first_name", "last_name", "roles", "tags")

    roles = ma.Nested(RoleSchema, many=True)
    tags = ma.Nested(TagSchema, many=True)


class TicketSchema(ma.Schema):
    class Meta:
        fields = (
            "ticket_id",
            "title",
            "body",
            "status",
            "votes_count",
            "student",
            "tags",
            "created_at",
            "updated_at",
        )

    student = ma.Nested(UserSchema)
    tags = ma.Nested(TagSchema, many=True)


class TicketSearchSchema(ma.Schema):
    class Meta:
        fields = (
            "ticket_id",
            "title",
            "body",
        )


class CommentSchema(ma.Schema):
    class Meta:
        # model = Comment
        fields = (
            "comment_id",
            "body",
            "created_at",
            "updated_at",
            "solution",
            "commentor",
        )

    commentor = ma.Nested(UserSchema)


class FaqsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Faqs


