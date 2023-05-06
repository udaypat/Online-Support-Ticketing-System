from main import app

JWT = ''
TICKET_ID = ''


def test_login():
    global JWT
    response = app.test_client().post('/api/user/login', json={
        "username": "craig_fox",
        "password": "password"
    })
    JWT = response.get_json()['access_token']
    assert response.status_code == 200


def test_get_tickets():
    response =  app.test_client().get(
        '/api/tickets?page=0&per_page=10', headers={'Authorization': 'Bearer ' + JWT})
    assert response.status_code == 200


def test_post_tickets():
    global TICKET_ID
    response =  app.test_client().post(
        '/api/tickets', headers={'Authorization': 'Bearer ' + JWT},
        json={
            "title": "Need help with Python",
            "body": "I'm having trouble understanding Python classes. Can someone help me?"
        })
    TICKET_ID = response.get_json()['ticket_id']
    print(TICKET_ID)
    assert response.status_code == 200


def test_get_ticket_by_id():
    response =  app.test_client().get(
        '/api/tickets/{}'.format(TICKET_ID), headers={'Authorization': 'Bearer ' + JWT})
    assert response.status_code == 200


def test_update_ticket_by_id():
    response =  app.test_client().put(
        '/api/tickets/{}'.format(TICKET_ID), headers={'Authorization': 'Bearer ' + JWT},
        json={
            "title": "UPDATED: Need help with Python",
            "body": "UPDATED: I'm having trouble understanding Python classes. Can someone help me?"
        })
    assert response.status_code == 200


def test_delete_ticket_by_id():
    response =  app.test_client().delete(
        '/api/tickets/{}'.format(TICKET_ID), headers={'Authorization': 'Bearer ' + JWT},
        json={
            "title": "UPDATED: Need help with Python",
            "body": "UPDATED: I'm having trouble understanding Python classes. Can someone help me?"
        })
    assert response.status_code == 204