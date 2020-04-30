


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    return app


@pytest.fixture
def client(app):
    return app.test_client()

def test_delete(client):
    resp = client.get('http://localhost:5000/DeleteMessage?applicationId=1')
    data = resp.json()
    assert data['success'] == 'True'



def add(client,application_id,session_id,message_id,content):
    return client.post('/AddMessage',data=dict(
    application_id=application_id,
    session_id=session_id,
    message_id=message_id,
    participants=["avi aviv", "moshe cohen"],
    content=content),
    follow_redirects=True)

def test_add(client):
    response = add(client, flaskr.app.config['aaaa'], flaskr.app.config['bbbb'], flaskr.app.config['aaa'], flaskr.app.config['Hi, how are yofsdgfu today?'])
    assert response.json['success'] == True   
# def test_add(client):
#     data = {
#     "application_id": "5",
#     "session_id": "aaaa",
#     "message_id": "bbbbb",
#     "participants": ["avi aviv", "moshe cohen"],
#     "content":"Hi, how are yofsdgfu today?"
# }
#     url = '/AddMessage/'

#     response = client.post(url, json=data)

#     assert response.json['success'] == True         