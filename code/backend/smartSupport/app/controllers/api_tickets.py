import requests
from datetime import datetime
from werkzeug.exceptions import Unauthorized

from sqlalchemy import desc, func
from flask import current_app as app
from flask import jsonify, request, Markup
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)

from app.data.db import db
from app.data.models import Ticket, Vote, Faqs, Comment, Tag, TicketSearch
from app.data.schema import TicketSchema, TicketSearchSchema
from app.utils.validation import *
from app.utils.auth import Auth, NotAuthorized
import app.utils.email as email

# jwt = JWTManager(app)
# salt = bcrypt.gensalt()

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
tickets_search_schema = TicketSearchSchema(many=True)


# get all tickets
@app.get("/api/tickets")
def get_tickets():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    vote_subquery = (
        db.session.query(Vote.ticket_id, func.count(Vote.vote_id).label("vote_count"))
        .group_by(Vote.ticket_id)
        .subquery()
    )

    sorted_tickets = (
        Ticket.query.join(vote_subquery, Ticket.ticket_id == vote_subquery.c.ticket_id)
        .order_by(
            Ticket.status.asc(),
            Ticket.created_at.asc(),
            vote_subquery.c.vote_count.desc(),
        )
        .limit(per_page)
        .offset(page * per_page)
        .all()
    )

    result = tickets_schema.dump(sorted_tickets)
    return jsonify(result), 200


# get all open tickets
@app.get("/api/tickets/open")
@jwt_required()
def get_open_tickets():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    vote_subquery = (
        db.session.query(Vote.ticket_id, func.count(Vote.vote_id).label("vote_count"))
        .group_by(Vote.ticket_id)
        .subquery()
    )

    sorted_tickets = (
        Ticket.query.join(vote_subquery, Ticket.ticket_id == vote_subquery.c.ticket_id)
        .filter(Ticket.status == "Open")
        .order_by(
            vote_subquery.c.vote_count.desc(),
            Ticket.created_at.desc(),
        )
        .limit(per_page)
        .offset(page * per_page)
        .all()
    )

    result = tickets_schema.dump(sorted_tickets)
    return jsonify(result), 200


# get all resolved or closed tickets
@app.get("/api/tickets/resolved-or-closed")
@jwt_required()
def get_resolved_closed_tickets():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    vote_subquery = (
        db.session.query(Vote.ticket_id, func.count(Vote.vote_id).label("vote_count"))
        .group_by(Vote.ticket_id)
        .subquery()
    )

    sorted_tickets = (
        Ticket.query.join(vote_subquery, Ticket.ticket_id == vote_subquery.c.ticket_id)
        .filter((Ticket.status == "Resolved") | (Ticket.status == "Closed"))
        .order_by(
            vote_subquery.c.vote_count.desc(),
            Ticket.created_at.desc(),
        )
        .limit(per_page)
        .offset(page * per_page)
        .all()
    )

    result = tickets_schema.dump(sorted_tickets)
    return jsonify(result), 200


# get open tickets for a support user
@app.get("/api/tickets/support/open")
@jwt_required()
def get_support_open_tickets():
    current_user_id = get_jwt_identity()
    user = db.session.query(User).filter(User.user_id == current_user_id).first()
    tag_list = user.tags

    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    tag_ids = [tag.tag_id for tag in user.tags]

    tickets = (
        Ticket.query.join(Ticket.tags)
        .filter(Tag.tag_id.in_(tag_ids), Ticket.status == "Open")
        .limit(per_page)
        .offset(page * per_page)
        .all()
    )
    tickets_sorted = sorted(tickets, key=lambda t: t.votes_count, reverse=True)

    result = tickets_schema.dump(tickets_sorted)
    return jsonify(result), 200


# get resolved and closed tickets for a support user
@app.get("/api/tickets/support/resolved-or-closed")
@jwt_required()
def get_support_resolved_closed_tickets():
    current_user_id = get_jwt_identity()
    user = db.session.query(User).filter(User.user_id == current_user_id).first()
    tag_list = user.tags

    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    tag_ids = [tag.tag_id for tag in user.tags]

    tickets = (
        Ticket.query.join(Ticket.tags)
        .filter(
            Tag.tag_id.in_(tag_ids),
            ((Ticket.status == "Resolved") | (Ticket.status == "Closed")),
        )
        .limit(per_page)
        .offset(page * per_page)
        .all()
    )
    tickets_sorted = sorted(tickets, key=lambda t: t.votes_count, reverse=True)

    result = tickets_schema.dump(tickets_sorted)
    return jsonify(result), 200


# get resolved and closed tickets for a support user
@app.get("/api/tickets/support/all")
@jwt_required()
def get_all_support_tickets():
    current_user_id = get_jwt_identity()
    user = db.session.query(User).filter(User.user_id == current_user_id).first()

    tag_ids = [tag.tag_id for tag in user.tags]

    tickets = Ticket.query.join(Ticket.tags).filter(Tag.tag_id.in_(tag_ids)).all()
    tickets_sorted = sorted(tickets, key=lambda t: t.votes_count, reverse=True)

    result = tickets_schema.dump(tickets_sorted)
    return jsonify(result), 200


# raise a new ticket
@app.post("/api/tickets")
@jwt_required()
def post_ticket():
    current_user_id = get_jwt_identity()
    ticketdata = request.get_json()

    title = ticketdata["title"]
    body = ticketdata["body"]
    tags = ticketdata["tags"]

    Validation.is_valid_string_value(title, "Title", alpha_only=False)
    Validation.is_valid_string_value(
        body, "Ticket Body", alpha_only=False, allow_special_chars=True
    )

    body = Markup(body)

    new_ticket = Ticket(title=title, body=body, student_id=current_user_id)

    for tagname in tags:
        tag = db.session.query(Tag).filter(Tag.name == tagname).first()
        if not tag:
            return jsonify("Tag {} not found".format(tagname))
        new_ticket.tags.append(tag)
        # print(tag)

    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 200


# get a ticket by its ticket_id
@app.get("/api/tickets/<ticket_id>")
@jwt_required()
def get_ticket(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket:
        return ticket_schema.jsonify(ticket), 200
    else:
        raise NotFound(status_code=404, msg="Ticket not found")


# edit a ticket
@app.put("/api/tickets/<ticket_id>")
@jwt_required()
def put_ticket(ticket_id):
    current_user_id = get_jwt_identity()
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    old_tags = ticket.tags

    if not ticket:
        raise NotFound(status_code=404, msg="Ticket not found")

    for tag in old_tags:
        ticket.tags.remove(tag)
        print("-------", tag)

    Auth.authorize(current_user_id, ticket.student_id)
    ticketdata = request.get_json()
    title = ticketdata["title"]
    body = ticketdata["body"]
    new_tags = ticketdata["tags"]

    Validation.is_valid_string_value(title, "Title", alpha_only=False)
    Validation.is_valid_string_value(
        body, "Blog Body", alpha_only=False, allow_special_chars=True
    )

    ticket.title = title
    ticket.body = Markup(body)
    db.session.add(ticket)
    db.session.commit()

    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    for tagname in new_tags:
        tag = db.session.query(Tag).filter(Tag.name == tagname).first()
        if not tag:
            return jsonify("Tag {} not found".format(tagname))
        ticket.tags.append(tag)
    db.session.add(ticket)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 200


# delete a ticket
@app.delete("/api/tickets/<ticket_id>")
@jwt_required()
def delete_ticket(ticket_id):
    current_user_id = get_jwt_identity()
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if str(ticket.student_id) != str(current_user_id):
        return jsonify("Not Authorized"), 401

    if ticket:
        votes = db.session.query(Vote).filter(Vote.ticket_id == ticket_id).all()
        for vote in votes:
            db.session.delete(vote)

        comments = (
            db.session.query(Comment).filter(Comment.ticket_id == ticket_id).all()
        )
        for comment in comments:
            db.session.delete(comment)

        db.session.delete(ticket)
        db.session.commit()
        return jsonify("Ticket Deleted"), 204
    else:
        raise NotFound(status_code=404, msg="Ticket not found")


# get ticket for current logged in user ***Added Temporarily
@app.get("/api/tickets/user")
@jwt_required()
def get_loggedin_user_tickets():
    # page = int(request.args.get("page"))
    # per_page = int(request.args.get("per_page"))

    curr_userid = get_jwt_identity()

    sorted_tickets = (
        db.session.query(Ticket)
        .filter(Ticket.student_id == curr_userid)
        .order_by(
            Ticket.status.asc(),
            Ticket.created_at.asc(),
        )
        .all()
    )

    result = tickets_schema.dump(sorted_tickets)
    return jsonify(result), 200


# close a ticket
@app.put("/api/tickets/<ticket_id>/close")
@jwt_required()
def close_ticket(ticket_id):
    current_user_id = get_jwt_identity()
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not Ticket:
        raise NotFound(status_code=404, msg="Ticket not found")

    if ticket.status == "Resolved":
        return jsonify("Ticket already resolved"), 400

    if ticket.status == "Closed":
        return jsonify("Ticket already closed"), 400

    if Auth.authorize_support(current_user_id) or Auth.authorize_admin(current_user_id):
        ticket.status = "Closed"
        db.session.add(ticket)
        db.session.commit()

        student = (
            db.session.query(User).filter(User.user_id == ticket.student_id).first()
        )
        email.send_email(
            "Ticket closure notification",
            """Your ticket with title: '{}' has been closed.
Please write to admin@smartTicket.edu in case you want to reopen it.
""".format(
                ticket.title
            ),
            student.email,
        )

        return ticket_schema.jsonify(ticket), 200
    else:
        raise NotAuthorized()


# convert a resolved ticket to a FAQ
@app.post("/api/tickets/<ticket_id>/faqs")
@jwt_required()
def ticket_to_faq(ticket_id):
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket.status != "Resolved":
        return jsonify("Can not convert unresolved ticket to FAQ"), 400

    faq = db.session.query(Faqs).filter(Faqs.query == ticket.body).first()
    if faq:
        return jsonify("FAQ already exists"), 400

    comment = (
        db.session.query(Comment)
        .filter(Comment.ticket_id == ticket_id, Comment.solution == 1)
        .first()
    )

    if not comment:
        return jsonify("Solution comment not found"), 404

    new_faq = Faqs(query=ticket.body, answer=comment.body)
    db.session.add(new_faq)
    db.session.commit()
    return jsonify(f"Ticket converted to FAQ successfully with faq_id {new_faq.faq_id}")


# search ticket
@app.get("/api/tickets/search")
@jwt_required()
def search_ticket():
    q = request.args.get("q")

    tickets = TicketSearch.query.filter(TicketSearch.body.op("MATCH")(q)).limit(5).all()
    results = tickets_search_schema.dump(tickets)

    return jsonify(results), 200


# send notification
@app.post("/api/tickets/notify")
@jwt_required()
def notify():
    current_user_id = get_jwt_identity()
    is_support = Auth.authorize_support(current_user_id)
    is_admin = Auth.authorize_admin(current_user_id)
    if not is_admin and not is_support:
        raise NotAuthorized()

    mail_data = request.get_json()
    recipient_email = mail_data["recipient_email"]
    message = mail_data["message"]

    Validation.is_valid_email(recipient_email, new_user=False)
    Validation.is_valid_string_value(
        message, "Email Body", alpha_only=False, allow_special_chars=True
    )

    email.send_email("Notification", message, recipient_email)

    return jsonify("Notification succesfully sent to email of the user"), 200


# assign ticket to user
@app.post("/api/tickets/assign")
@jwt_required()
def assign_ticket():
    ticket_data = request.get_json()

    ticket_id = ticket_data["ticket_id"]
    username_to_assign_to = ticket_data["username"]

    assignee = (
        db.session.query(User).filter(User.username == username_to_assign_to).first()
    )

    message = "Please look into the issues mentioned in the Ticket identified by ticket_id: {} and provide neccessary resolution.".format(
        ticket_id
    )
    email.send_email("Ticket Assignment", message, assignee.email)

    return jsonify("Ticket assignment done successfully"), 200
