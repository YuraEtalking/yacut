"""Эндпоинты REST API для сервиса сокращения ссылок."""

from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import ApiException
from .models import URLMap
from .utility import build_short_url
from .validators import validate_api_response


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Возвращает исходный URL по короткому идентификатору."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise ApiException(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )

    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def shorten_url():
    """Создаёт короткую ссылку и возвращает данные сокращения."""
    data = request.get_json(silent=True)
    valid_data = validate_api_response(data)
    url = URLMap()
    url.from_dict(valid_data)
    db.session.add(url)
    db.session.commit()
    return jsonify({
        'url': url.original,
        'short_link': build_short_url(url.short)
    }), HTTPStatus.CREATED
