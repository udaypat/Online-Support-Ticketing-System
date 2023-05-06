from flask import current_app as app

from app.data.models import Role
from app.data.db import db


@app.post('/fake/roles')
def fake_roles():    
    roles = ['Admin', 'Support', 'Student']

    for role in roles:
        new_role = Role(name=role)
        db.session.add(new_role)	
        db.session.commit()

    return 'Success', 200