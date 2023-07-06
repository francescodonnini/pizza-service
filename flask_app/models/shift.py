from flask_app import db


class Workday(db.Model):
    __tablename__ = 'workday_table'
    day = db.Column(db.Date, primary_key=True)
    plan = db.Column(db.Integer, db.ForeignKey('plan_table.id'), primary_key=True)
    minNumberOfRider = db.Column(db.Integer, nullable=False)
    maxNumberOfRider = db.Column(db.Integer, nullable=False)

    def __init__(self, day, plan, min_number_rider, max_number_rider):
        self.day = day
        self.plan = plan
        self.minNumberOfRider = min_number_rider
        self.maxNumberOfRider = max_number_rider

    def __repr__(self):
        return f'<Workday {self.day}, {self.plan}, {self.numberOfRider}>'


class Shift(db.Model):
    __tablename__ = 'shift_table'
    day = db.Column(db.Date, primary_key=True)
    plan = db.Column(db.Integer, primary_key=True)
    rider = db.Column(db.String(256), db.ForeignKey('users_table.email'), primary_key=True)
    __table_args__ = (db.ForeignKeyConstraint([day, plan], [Workday.day, Workday.plan]), )

    def __init__(self, day, plan, rider):
        self.day = day
        self.plan = plan
        self.rider = rider

    def __repr__(self):
        return f'<Shift {self.day}, {self.plan}, {self.rider}>'


class Plan(db.Model):
    __tablename__ = 'plan_table'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'<Plan {self.id}, {self.start}, {self.end}>'


