import enum

from werkzeug.security import generate_password_hash

from flask_app import db
from flask_app.models.constraint import Constraint


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
    max_num_of_shifts = db.Column(db.Integer)
    min_num_of_shifts = db.Column(db.Integer)
    constraints = db.relationship('Constraint', lazy=True)

    def __repr__(self):
        return f'<User {self.email}, {self.name}, {self.last_name}>'

    def validate(self, pw):
        return self.pw_hash == generate_password_hash(pw)

    def set_password(self, pw):
        self.pw_hash = generate_password_hash(pw)

    def __init__(self, email, last_name, name, role):
        self.email = email
        self.last_name = last_name
        self.name = name
        self.role = role


def user2json(user: User) -> dict[str, object]:
    constraints: list[dict[str, object]] = []
    if user.role == Role.rider:
        def constraint_mapper(c: Constraint) -> dict[str, object]:
            return {
                'category': c.category.name,
                'date': c.date.isoformat(),
                'occurrence': c.occurrence.name
            }

        for c in user.constraints:
            constraints.append(constraint_mapper(c))
    return {
        'email': user.email,
        'last_name': user.last_name,
        'name': user.name,
        'role': user.role.name,
        'constraints': constraints,
        'max_num_of_shifts': user.max_num_of_shifts,
        'min_num_of_shifts': user.min_num_of_shifts
    }
