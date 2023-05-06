from flask import current_app as app

from app.data.models import Tag
from app.data.db import db


@app.post('/fake/tags')
def fake_tags():    
    tags = ['SoftEng', 'SoftTest', 'DeepLearn', 'ArtInt', 'FinFor', 'Ops', 'Clarification', 'Assignment']

    for tag in tags:
        new_tag = Tag(name=tag)
        db.session.add(new_tag)	
        db.session.commit()

    return 'Success', 200