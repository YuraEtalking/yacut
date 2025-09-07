from http import HTTPStatus
from flask import abort, flash, redirect, render_template, request, url_for, jsonify
from sqlalchemy.exc import IntegrityError

from . import app, db
from .error_handlers import BadRequestAPI
from .forms import UrlForm
from .models import URLMap
from .utility import get_unique_short_id, get_short_link


@app.route('/api/id/', methods=['POST'])
def shorten_url():

    data = request.get_json(silent=True)
    if data is None:
        raise BadRequestAPI('Отсутствует тело запроса')

    elif 'url' not in data:
        raise BadRequestAPI(r'\"url\" является обязательным полем!')

    elif len(data['custom_id']) == 0: # todo сделай валидацию нормально с re)
        raise BadRequestAPI('Указано недопустимое имя для короткой ссылки')

    elif URLMap.query.filter_by(original=data['url']).first() is not None:
        raise BadRequestAPI('Предложенный вариант короткой ссылки уже существует.')

    print(f'что там: {data}')
    url_in_db = URLMap.query.filter_by(original=data['url']).first()
    if url_in_db is not None:
        return jsonify({
            'url': url_in_db.original,
            'short_link': get_short_link(url_in_db.short)
        }), HTTPStatus.OK

    data['original'] = data.pop('url')
    data['short'] = data.pop('custom_id')
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify({
        'url': url.original,
        'short_link': get_short_link(url.short)
    }), HTTPStatus.CREATED