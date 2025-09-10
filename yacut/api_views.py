"""Эндпоинты REST API для сервиса сокращения ссылок."""

from http import HTTPStatus
from typing import Any

from flask import jsonify, request, Response

from . import app
from .error_handlers import ApiException, ShortIdAlreadyExistsError
from .models import URLMap
from .validators import validate_api_response


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id: str) -> tuple[Response, int]:
    """Возвращает исходный URL по короткому идентификатору."""
    url = URLMap.get_by_short(short_id).first()
    if url is None:
        raise ApiException(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )

    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def shorten_url() -> tuple[Response, int]:
    """Создаёт короткую ссылку и возвращает данные сокращения."""
    try:
        data: dict[str, Any] | None = request.get_json(silent=True)
        valid_data = validate_api_response(data)
        url = URLMap.create_or_generate_shortcode(valid_data)
    except ShortIdAlreadyExistsError as e:
        raise e
    return jsonify({
        'url': url.original,
        'short_link': URLMap.build_short_url(url.short)
    }), HTTPStatus.CREATED
