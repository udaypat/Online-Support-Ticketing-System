import bcrypt

from faker import Faker
from flask import current_app as app
# from flask_security.utils import hash_password

from app.data.models import *
from app.data.db import db

f = Faker()


@app.post('/fake/users')
def fake_users():
    n = int(input('How many?????????????????'))
    for i in range(n):
        name = f.unique.name()
        first_name = name.split()[0]
        last_name = name.split()[1]
        username = name.replace(' ', '_')
        username = username.lower()
        # password = hash_password('pass')
        password = 'password'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        email = '{}@mail.com'.format(username)
        fs_uniquifier = f.uuid4()
        user = User(username=username, email=email, password=password_hash, first_name=first_name,
                    last_name=last_name, fs_uniquifier=fs_uniquifier)

        users = User.query.all()
        usernames = [user.username for user in users]

        if username not in usernames:
            db.session.add(user)
            db.session.commit()
            # print('---')
            print(first_name, username, email)

    users = db.session.query(User).all()
    admin_role = db.session.query(Role).filter(Role.name == 'Admin').first()
    support_role = db.session.query(Role).filter(Role.name == 'Support').first()
    student_role = db.session.query(Role).filter(Role.name == 'Student').first()

    count = 0
    for user in users:
        count+= 1
        if (len(user.roles) == 0):
            user.roles.append(student_role)
        if (count%9 == 0):
            user.roles.append(support_role)
        if (count%16 == 0):
            user.roles.append(admin_role)

        db.session.add(user)
        db.session.commit()
        print(count)
    return 'Success', 200



@app.post('/fake/users')
def fake_user_tags():
    roles = ['Admin', 'Support']

    users = User.query.join(User.roles).filter(Role.name.in_(roles)).all()
    userids = [user.user_id for user in users]

    tags = Tag.query.all()
    tagids = [tag.tag_id for tag in tags]

    for (tag, user) in zip(tags, users):
        user.tags.append(tag)
        db.session.add(user)
        db.session.commit()
        print(tag, user)

