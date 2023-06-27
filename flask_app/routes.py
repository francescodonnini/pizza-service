from flask import jsonify, abort, request

from flask_app import app, db
from flask_app.models.user import Role, User, user2json
from sqlalchemy import exc


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
        return jsonify({
            'code': e.code,
        })
