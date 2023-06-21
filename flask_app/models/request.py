import enum

from flask_app import db


class Request(db.Model):
    __tablename__ = 'requests_table'
    source = db.Column(db.String(256), db.ForeignKey('users_table.email'), primary_key=True, nullable=False)
    date = db.Column(db.Date, primary_key=True, nullable=False)

    def __repr__(self):
        return f'<Request {self.source}, {self.date}>'


class Response(enum.Enum):
    dismissed = 'dismissed'
    read = 'read'


class RequestStat(db.Model):
    __tablename__ = 'request_stats_table'
    date = db.Column(db.Date, primary_key=True, nullable=False)
    source = db.Column(db.String(256), primary_key=True, nullable=False)
    recipient = db.Column(db.String(256), db.ForeignKey('users_table.email'), primary_key=True, nullable=False)
    response = db.Column(db.Enum(Response), nullable=False)
    __table_args__ = (db.ForeignKeyConstraint([date, source], [Request.date, Request.source]), )