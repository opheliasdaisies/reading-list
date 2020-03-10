from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, post_load, validate, validates_schema, ValidationError, EXCLUDE


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def _repr_(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def validate_unique_username(username):
    if User.query.filter_by(username=username).first():
        raise ValidationError("Username already exists.")

def validate_unique_email(email):
    if User.query.filter_by(email=email).first():
        raise ValidationError("Email already exists.")


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        unknown = EXCLUDE

    id = ma.auto_field()
    username = ma.String(required=True, validate=[validate.Length(min=1, max=80), validate_unique_username])
    email = ma.Email(required=True, validate=[validate.Length(min=1, max=120), validate_unique_email])
    password = ma.auto_field(column_name='password_hash', load_only=True, required=True, validate=[validate.Length(min=8, max=128)])
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)

    @post_load
    def create_user(self, data, **kwargs):
        user = User(**data)
        user.set_password(data['password_hash'])
        return user
