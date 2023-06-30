from flask import abort, request

from flask_app.models.user import Role, User, user2json
from flask_app.models.request import *
from flask_app.errors import *
from datetime import datetime
from flask_app.models.shift import *
from flask_app.models.constraint import *
from sqlalchemy import and_, or_


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    pw = request.json['password']
    user = db.User.query.filter_by(email=email).first()
    if user is not None and user.validate(pw):
        return user2json(user)
    else:
        abort(404)


@app.route('/riders', methods=['GET'])
def riders():
    rider_list = User.query.filter_by(role=Role.rider)
    json = []
    for r in rider_list:
        json.append(user2json(r))
    return jsonify(json)


@app.route('/requests', methods=['POST'])
def requests():
    pass


@app.route('/save_rider', methods=['POST'])
def save_rider():
    first_name = request.json['firstName']
    last_name = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    user = User(email, last_name, first_name, Role.rider)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({
            'code': "200",
            'message': "Rider has been submitted"
        })
    except exc.IntegrityError as e:
        return rider_already_exists(e)


@app.route('/add_constraint', methods=['POST'])
def add_constraint():
    rider = request.json['email']
    category = request.json['category']
    date = request.json['date']
    occurrence = request.json['occurrence']
    user = db.session.query(User).filter_by(email=rider).first()
    if user is not None:
        constraint = Constraint(rider, category, occurrence, datetime.strptime(date, '%Y-%m-%d'))
        db.session.add(constraint)
        db.session.commit()
        return jsonify({
            'code': "200",
            'message': "Constraint has been submitted"
        })
    else:
        return jsonify({
            'code': "450",
            'message': "Unknown user"
        })


@app.route('/add_request', methods=['POST'])
def add_request() :
    rider = request.json['email']
    date = request.json['date']
    user = db.session.query(User).filter_by(email=rider).first()
    if user is not None:
        change_request = Request(rider, datetime.strptime(date, '%Y-%m-%d'))
        db.session.add(change_request)
        db.session.commit()
        return jsonify({
            'code': "200",
            'message': "Request has been submitted"
        })
    else:
        return jsonify({
            'code': "450",
            'message': "Unknown user"
        })


@app.route('/show_new_requests', methods=['GET', 'POST'])
def show_new_requests():
    recipient = request.json['email']
    new_requests = db.session.query(Request).all()
    json = []
    for n in new_requests:
        json.append(request2json(n))
        stat = RequestStat(n.date, n.source, recipient, Response.read)
        db.session.add(stat)
    db.session.commit()
    return jsonify(json)


@app.route('/accept_request', methods=['POST'])
def accept_request():
    recipient = request.json['recipient']
    source = request.json['source']
    date = datetime.strptime(request.json['date'], '%Y-%m-%d')
    req = db.session.query(Request).filter(and_(Request.source == source, Request.date == date.strftime('%Y-%m-%d'))).first()
    read_reqs = db.session.query(RequestStat).filter(and_(RequestStat.source == source, RequestStat.date == date.strftime('%Y-%m-%d'))).all()
    for rr in read_reqs:
        db.session.delete(rr)
    plan = db.session.query(Plan).filter(and_(date.strftime('%Y-%m-%d') >= Plan.start, date.strftime('%Y-%m-%d') <= Plan.end)).first()
    if plan is None:
        return jsonify({
            'code': "451",
            'message': "Unknown plan"
        })
    shift = Shift(date, plan.id, recipient)
    db.session.add(shift)
    db.session.delete(req)
    db.session.commit()
    return jsonify({
        'code': "200",
        'message': "You have a new shift"
    })


@app.route('/get_constraints', methods=['POST'])
def get_constraints():
    rider = request.json['email']
    constraints = db.session.query(Constraint).filter_by(rider=rider).all()
    j_constraints = []
    for c in constraints:
        j_constraints.append(constraint_mapper(c))
    return jsonify(j_constraints)


@app.route('/delete_constraint', methods=['POST'])
def delete_constraint():
    date = datetime.strptime(request.json['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    rider = request.json['email']
    constraint = db.session.query(Constraint).filter(and_(Constraint.date == date, Constraint.rider == rider)).first()
    if constraint is None:
        return jsonify({
            'code': "452",
            'message': "You have not a constraint for the date specified"
        })
    db.session.delete(constraint)
    db.session.commit()
    return jsonify({
        'code': "200",
        'message': "Constraint correctly removed"
    })


@app.route('/fire_rider', methods=['POST'])
def fire_rider():
    email = request.json["email"]
    rider = db.session.query(User).filter_by(email=email).first()
    if rider is None:
        return jsonify({
            'code': "450",
            'message': "Unknown user"
        })
    shifts = db.session.query(Shift).filter_by(rider=email).all()
    if shifts is not None:
        for s in shifts:
            db.session.delete(s)
    req = db.session.query(Request).filter_by(source=email).all()
    if req is not None:
        for r in req:
            db.session.delete(r)
    req_stat = db.session.query(RequestStat).filter(or_(RequestStat.source == email, RequestStat.recipient == email)).all()
    if req_stat is not None:
        for rs in req_stat:
            db.session.delete(rs)
    constraints = db.session.query(Constraint).filter_by(rider=email).all()
    if constraints is not None:
        for c in constraints:
            db.session.delete(c)
    db.session.delete(rider)
    db.session.commit()
    return jsonify({
        'code': "200",
        'message': "Rider correctly removed"
    })

