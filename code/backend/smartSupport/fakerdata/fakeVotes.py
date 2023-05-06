import random

from faker import Faker
from flask import current_app as app
from flask import  render_template
from .fakeTickets import random_date

from app.data.models import *
from app.data.db import db

f = Faker()

# Set the start and end dates
start = datetime(2020, 1, 1)
end = datetime(2023, 2, 28)

@app.route('/fake/votes', methods=["GET"])
def fake_votes():    
    users = db.session.query(User).all()
    tickets = db.session.query(Ticket).all()
    ticket_user = []
    
    n = int(input('How many?????????????????'))
    for i in range(n):
        user = random.choice(users)
        ticket = random.choice(tickets)
        created_at = random_date(start, end)

        if (ticket, user) not in ticket_user:
            new_vote = Vote(ticket_id=ticket.ticket_id, user_id=user.user_id, created_at=created_at)
            db.session.add(new_vote)	
            db.session.commit()
            ticket_user.append((ticket, user))
            print((ticket, user))

    return 'Success', 200


