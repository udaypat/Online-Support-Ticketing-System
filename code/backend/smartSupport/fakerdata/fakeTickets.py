import datetime, random
from datetime import timedelta

from faker import Faker
from flask import current_app as app

from app.data.models import *
from app.data.db import db

f = Faker()


def random_date(start, end):    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

# Set the start and end dates
start = datetime(2020, 1, 1)
end = datetime(2023, 2, 28)


@app.post('/fake/tickets')
def fake_tickets():
    ticket_lengths = [15, 6, 20, 8, 12]
    ticket_status = ['Open', 'Resolved']    

    roles_to_exclude = ['Admin', 'Support']
    students = User.query.join(User.roles).filter(~User.roles.any(Role.name.in_(roles_to_exclude))).all()

    n = int(input('How many?????????????????'))
    for i in range(n):
        ticket_length = random.choice(ticket_lengths)        
        status = random.choice(ticket_status)
        title = f.sentence()        
        student = random.choice(students)
        created_at = random_date(start, end)
        updated_at = random_date(created_at, end)
        body = ''
        for _ in range(ticket_length):
            body += ' ' + f.sentence()

        new_ticket = Ticket(student_id=student.user_id, title=title, body=body, status=status, created_at=created_at, 
                            updated_at=updated_at)
        db.session.add(new_ticket)	
        db.session.commit()
        print(student.user_id, status, title, created_at, updated_at,  body)    
        print('====================================================')
    return 'Success', 200

   

@app.post('/fake/tickets/add/tags')
def add_tags():
    tag_counts = [1, 2, 3]
    tags = Tag.query.all()
    taglist = [tag for tag in tags]

    tickets = Ticket.query.all()

    for ticket in tickets:
        tag_count = random.choice(tag_counts)
        tags = []
        for count in range(tag_count):
            tag = random.choice(taglist)
            if tag not in tags:
                tags.append(tag)
                ticket.tags.append(tag)
        db.session.add(ticket)	
        db.session.commit()    
        print(ticket.ticket_id, tags)

 

