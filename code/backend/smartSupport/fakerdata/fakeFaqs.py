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


@app.post('/fake/faqs')
def fake_faqs():
    faq_lengths = [15, 6, 20, 8, 12]        

    n = int(input('How many?????????????????'))
    for i in range(n):
        faq_length = random.choice(faq_lengths) 
        query = f.sentence()                
        created_at = random_date(start, end)
        updated_at = random_date(created_at, end)
        answer = ''
        for _ in range(faq_length):
            answer += ' ' + f.sentence()

        new_faq = Faqs(query=query, answer=answer, created_at=created_at, updated_at=updated_at)
        db.session.add(new_faq)	
        db.session.commit()
        print(query, created_at, updated_at,  answer)    
        print('====================================================')
    return 'Success', 200