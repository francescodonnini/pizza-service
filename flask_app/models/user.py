import enum

from werkzeug.security import generate_password_hash

from flask_app import db


class Role(enum.Enum):
    admin = 'admin'
    rider = 'rider'


class User(db.Model):
    __tablename__ = 'users_table'
    email = db.Column(db.String(256), primary_key=True)
    last_name = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    pw_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(Role, native_enum=True), nullable=False)
    max_num_of_shifts = db.Column(db.Integer, nullable=False)
    min_num_of_shifts = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.email}, {self.name}, {self.last_name}>'

    def validate(self, pw):
        return self.pw_hash == generate_password_hash(pw)

    def set_password(self, pw):
        self.pw_hash = generate_password_hash(pw)
