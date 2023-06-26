import werkzeug.exceptions
from flask import jsonify
from werkzeug.exceptions import HTTPException

from flask_app import app


class InvalidCredentials(HTTPException):
    code = 480
    description = 'wrong email or password'


@app.errorhandler(InvalidCredentials)
def invalid_credentials(e):
    return jsonify({
        'code': e.code,
        'description': e.description
    })
