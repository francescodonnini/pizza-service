from flask import jsonify, abort, request

from flask_app.models.constraint import Constraint
from flask_app.models.request import Request, RequestStat
from flask_app.models.user import Role
from flask_app import app, db


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello'


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    pw = request.json['password']
    user = db.User.query.filter_by(email=email).first()
    if user is not None and user.validate(pw):
        return user2json(user)
    else:
        abort(404)


def user2json(user):
    constraints = []
    if user.role == Role.rider:
        def constraint_mapper(c: Constraint):
            return jsonify({
                'category': c.category,
                'date': c.date,
                'occurrence': c.occurrence
            })

        constraints += user.constraints.map(constraint_mapper)
    return jsonify({
        'email': user.email,
        'last_name': user.last_name,
        'name': user.name,
        'role': user.role.name,
        'constraints': constraints,
        'max_num_of_shifts': user.max_num_of_shifts,
        'min_num_of_shifts': user.min_num_of_shifts
    })


@app.route('/riders', methods=['POST', 'GET'])
def riders():
    pass


@app.route('/requests', methods=['POST'])
def requests():
    pass
