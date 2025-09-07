from http import HTTPStatus
from flask import jsonify, render_template

from . import app, db

class HttpApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message = self.message)

class HttpException(HttpApiError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

class ApiException(HttpApiError):
    status_code = HTTPStatus.BAD_REQUEST


@app.errorhandler(ApiException)
def api_error(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HttpException)
def http_error(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
