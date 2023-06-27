from flask import jsonify
from werkzeug.exceptions import HTTPException

from flask_app import app
from sqlalchemy import exc


class InvalidCredentials(HTTPException):
    code = 480
    description = 'wrong email or password'


class RiderAlreadyExists(exc.IntegrityError):
    code = 309
    description = 'rider already exists'


@app.errorhandler(InvalidCredentials)
def invalid_credentials(e):
    return jsonify({
        'code': e.code,
        'description': e.description
    })


@app.errorhandler(RiderAlreadyExists)
def rider_already_exists(e):
    return jsonify({
        'code': e.code,
        'description' : e.description
    })
