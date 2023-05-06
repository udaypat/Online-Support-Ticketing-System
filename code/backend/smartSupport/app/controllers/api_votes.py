from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.data.db import db
from app.data.models import Vote, Ticket
from app.data.schema import TicketSchema
from app.utils.auth import Auth, NotAuthorized


ticket_schema = TicketSchema()

# Upvote a ticket
@app.post("/api/tickets/<ticket_id>/upvote")
@jwt_required()
def upvote_ticket(ticket_id):
    current_user_id = get_jwt_identity()

    vote = db.session.query(Vote).filter(
        Vote.ticket_id == ticket_id, Vote.user_id==current_user_id).first()

    if not vote:
        new_vote = Vote(ticket_id=ticket_id, user_id=current_user_id)
        db.session.add(new_vote)
        db.session.commit()

        ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        result = ticket_schema.dump(ticket)
        return jsonify(result), 200
    else:
        return jsonify("Already upvoted"), 400



# Revote vote from a ticket
@app.delete("/api/tickets/<ticket_id>/revoke-vote")
@jwt_required()
def revoke_vote_from_ticket(ticket_id):
    current_user_id = get_jwt_identity()

    vote = db.session.query(Vote).filter(
        Vote.ticket_id == ticket_id, Vote.user_id==current_user_id).first()

    if vote:
        db.session.delete(vote)
        db.session.commit()

        return jsonify("Vote revoked successfully"), 200
    else:
        return jsonify("No vote present to revoke"), 404