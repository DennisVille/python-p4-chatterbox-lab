from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        mess_ages = Message.query.order_by(Message.created_at).all()
        mess_dict = [mess.to_dict() for mess in mess_ages]

        return make_response(mess_dict, 200)
    elif request.method == "POST":
        new_message_data = request.get_json()
        new_message = Message(
            body = new_message_data.get('body'),
            username = new_message_data.get('username'))
        
        db.session.add(new_message)
        db.session.commit()

        response_body = new_message.to_dict()
        return make_response(response_body, 200)
    

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    the_message = Message.query.filter_by(id = id).first()
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(the_message, attr, data[attr])
        
        db.session.add(the_message)
        db.session.commit()

        response_body = the_message.to_dict()
        return make_response(response_body, 200)
    
    elif request.method == "DELETE":
        db.session.delete(the_message)
        db.session.commit()

        response_body = {'delete successful': True}
        return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555)
