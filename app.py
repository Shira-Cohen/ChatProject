from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    message_id = db.Column(db.String(200))
    application_id = db.Column(db.String(200), nullable=False)
    session_id = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    participants = db.Column(db.PickleType, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/GetMessage')
def GetMessage():
    messages = Message.query.all()
    application_id = request.args.get('applicationId')
    if application_id:
        messages = Message.query.filter_by(application_id=application_id).all()
    message_id = request.args.get('messageId')
    if message_id:
        messages = Message.query.filter_by(message_id=message_id).all()
    session_id = request.args.get('sessionId')
    if session_id:
        messages = Message.query.filter_by(session_id=session_id).all()
    all_messages = [{'message_id':m.message_id,'application_id':m.application_id,'session_id':m.session_id,'content':m.content,'participants':m.participants} for m in messages]
    return jsonify(all_messages)

    return json.dumps([(dict(row.items())) for row in messages])

@app.route('/DeleteMessage')
def DeleteMessage():
    messages = Message.query.all()
    application_id = request.args.get('applicationId')
    if application_id:
        Message.query.filter_by(application_id=application_id).delete()
    message_id = request.args.get('messageId')
    if message_id:
        messages = Message.query.filter_by(message_id=message_id).delete()
    session_id = request.args.get('sessionId')
    if session_id:
        messages = Message.query.filter_by(session_id=session_id).delete()
        print(messages)
    try:
        db.session.commit()
        return jsonify(success=True)
    except:
        return jsonify(success=False)
        


@app.route('/AddMessage', methods=['POST'])
def AddMessage():
    content = request.get_json()
    new_message = Message(content=content['content'], 
     application_id=content['application_id'],
     session_id=content['session_id'], 
     participants=content['participants'],
     message_id=content['message_id'])
    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify(success=True)
    except:
        return jsonify(success=False)



if __name__ == "__main__":
    app.run(debug=True)
