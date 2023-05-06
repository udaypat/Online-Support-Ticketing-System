from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from .db import db


user_tags = db.Table(
    "user_tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.tag_id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True),
    UniqueConstraint("user_id", "tag_id", name="user_tag"),
)


ticket_tags = db.Table(
    "ticket_tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.tag_id"), primary_key=True),
    db.Column(
        "ticket_id", db.Integer, db.ForeignKey("ticket.ticket_id"), primary_key=True
    ),
    UniqueConstraint("ticket_id", "tag_id", name="ticket_tag"),
)

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.user_id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.role_id")),
    UniqueConstraint("user_id", "role_id", name="user_role"),
)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=True)
    fs_uniquifier = db.Column(db.String, nullable=False)
    # One-to-many relationship with Tickets
    tickets = db.relationship("Ticket", backref="student", lazy=True)
    # One-to-many relationship with Comments
    comments = db.relationship(
        "Comment",
        backref="commentor",
        order_by="desc(Comment.created_at)",
        lazy="dynamic",
        cascade="delete",
    )
    # One-to-many relationship with Votes
    votes = db.relationship("Vote", backref="voter", lazy=True, cascade='delete')
    # Many-to-many relationship with Tags
    tags = db.relationship("Tag", secondary="user_tags", backref="users", lazy=True)
    # Many-to-many relationship with Roles
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    # def __init__(self, username, email, first_name, last_name, password, fs_uniquifier):
    #     self.username = username
    #     self.email = email
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.password = password
    #     self.fs_uniquifier = fs_uniquifier


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Open")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # One-to-many relationship with Comments
    comments = db.relationship(
        "Comment",
        backref="ticket",
        order_by="desc(Comment.created_at)",
        lazy=True,
        cascade="delete",
    )
    # One-to-many relationship with Votes
    votes = db.relationship("Vote", backref="ticket", lazy="dynamic")
    # Many-to-many relationship with Tags
    tags = db.relationship("Tag", secondary="ticket_tags", backref="tickets", lazy=True)

    @property
    def votes_count(self):
        return self.votes.count()


class TicketSearch(db.Model):
    __tablename__ = 'ticket_search'
    ticket_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.ticket_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.ticket_id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)


class Faqs(db.Model):
    faq_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
