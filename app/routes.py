from app import app, db
from app.models.user import User, UserSchema
from flask import request, jsonify
from marshmallow import ValidationError

user_schema = UserSchema()

# SQLAlchemy's get_or_404 query returns html. This overwrites the default
# behavior so that a JSON response will be returned by default.
@app.errorhandler(404)
def not_found(error):
    response = jsonify({'code': 404, 'message': 'Not found'}), 404
    return response

@app.route('/')
def hello_world():
    return jsonify({'text': 'Hello World!!!'})

@app.route('/users', methods=['POST'])
@app.route('/users/', methods=['POST'])
def create_user():
    user_data = request.get_json()
    try:
        # TODO: Move this into marshmallow validation in the schema. I ran into some weird/unexpected
        # behavior, so will come back to this and improve the validation later.
        if not user_data['password'] or not user_data['password2'] or user_data['password'] != user_data['password2']:
            raise ValidationError('Passwords do not match.', 'password')
        new_user = user_schema.load(user_data)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/users/<int:id>', methods=['GET'])
@app.route('/users/<int:id>/', methods=['GET'])
def get_user(id):
    user_obj = User.query.get_or_404(id)
    deserialized_data = user_schema.dump(user_obj)
    return jsonify(deserialized_data), 200

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id, data):
    pass

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass
