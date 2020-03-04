import json
from app import app, db
from app.models import *
from flask import request


@app.route('/')
def hello_world():
    return json.dumps({'text': 'Hello World!!!'})

@app.route('/users', methods=['POST'])
def create_user():
    user_schema = user.UserSchema()
    data = request.get_json()
    new_user = user.User(username=data['username'], email=data['email'])
    # make sure password1 and password2 are the same
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return user_schema.dump(new_user)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id, data):
    pass

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass
