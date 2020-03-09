from app import app, db
from app.models import *
from flask import request, jsonify
from marshmallow import ValidationError, EXCLUDE


@app.route('/')
def hello_world():
    return jsonify({'text': 'Hello World!!!'})

@app.route('/users', methods=['POST'])
def create_user():
    user_schema = user.UserSchema()
    user_data = request.get_json()
    try:
        # TODO: Move this into marshmallow validation in the schema. I ran into some weird/unexpected
        # behavior, so will come back to this and improve the validation later.
        if not user_data['password'] or not user_data['password2'] or user_data['password'] != user_data['password2']:
            raise ValidationError('Passwords do not match.', 'password')
        new_user = user_schema.load(user_data, unknown=EXCLUDE)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id, data):
    pass

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass
