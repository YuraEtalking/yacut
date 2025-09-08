import re

from .error_handlers import ApiException
from .models import URLMap
from .utility import get_unique_short_id
from  .constants import MAX_LENGTH_SHORT_FIELD


def validate_api_response(data):
    short_pattern = r'^[A-Za-z0-9]+$'
    # Паттерн валидатора URL из WTForms, что бы соответствовать форме.
    url_pattern = (
            r"^[a-z]+://"
            r"(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )

    if data is None:
        raise ApiException('Отсутствует тело запроса')

    elif 'url' not in data or not data['url']:
        raise ApiException('"url" является обязательным полем!')

    elif not re.fullmatch(url_pattern, data['url']):
        raise ApiException('Недопустимое имя для "url"')

    custom_id = data.get('custom_id')
    if custom_id:
        if (not re.fullmatch(short_pattern, data['custom_id'])
              or len(data['custom_id']) > MAX_LENGTH_SHORT_FIELD):
            raise ApiException('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(original=data['url']).first() is not None:
            raise ApiException(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        data['custom_id'] = get_unique_short_id(data['url'])

    data['original'] = data.pop('url')
    data['short'] = data.pop('custom_id')

    return data