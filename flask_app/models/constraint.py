import enum

from flask_app import db


class Category(enum.Enum):
    absolute = 'absolute'
    relative = 'relative'

    def __repr__(self):
        return self.name


class Occurrence(enum.Enum):
    never = 'never'
    weekly = 'weekly'
    monthly = 'monthly'
    yearly = 'yearly'

    def __repr__(self):
        return self.name


class Constraint(db.Model):
    __tablename__ = 'constraints_table'
    id = db.Column(db.Integer, primary_key=True)
    rider = db.Column(db.String, db.ForeignKey('users_table.email'), nullable=False)
    category = db.Column(db.Enum(Category, native_enum=True), nullable=False)
    occurrence = db.Column(db.Enum(Occurrence), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Constraint {self.rider}, {self.category} {self.occurrence} {self.date}>'
