import random

from datetime import datetime
from faker import Faker
from flask import current_app as app

from app.data.models import Comment, Ticket, User
from app.data.db import db

from .fakeTickets import random_date

f = Faker()

# Set the start and end dates
start = datetime(2020, 1, 1)
end = datetime(2023, 2, 28)


@app.route('/fake/comments', methods=["GET"])
def fake_comments():
    comment_lengths = [2, 3, 4, 5]
    comment_counts = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]
    users = db.session.query(User).all()
    tickets = db.session.query(Ticket).all()

    for ticket in tickets:
        comment_length = random.choice(comment_lengths)
        comment_count = random.choice(comment_counts)

        for _ in range(comment_count):
            user = random.choice(users)
            created_at = random_date(start, end)
            updated_at = random_date(created_at, end)
            body = ''
            for _ in range(comment_length):
                body += ' ' + f.sentence()

            new_comment = Comment(
                user_id=user.user_id, ticket_id=ticket.ticket_id, body=body,
                created_at=created_at, updated_at=updated_at)

            print(ticket.ticket_id, user.user_id, body, created_at)
            print('====================================================')
            db.session.add(new_comment)
            db.session.commit()
    return 'Success', 200


@app.route('/fake/comments/mark/solutions', methods=["GET"])
def mark_solutions():
    closed_ticekts = Ticket.query.filter(Ticket.status == 'Resolved')
    for ticket in closed_ticekts:
        comments = ticket.comments
        comment_list = [comment for comment in comments]
        if len(comment_list) > 0:
            solution_comment = random.choice(comment_list)
            solution_comment.solution = 1
            db.session.add(solution_comment)
            db.session.commit()

            print(ticket.ticket_id)
            print(comment_list)
            print('====================================================')
    return 'Success', 200
