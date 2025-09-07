import re

from .error_handlers import ApiException
from .models import URLMap
from .utility import get_unique_short_id
from  .constants import MAX_LENGTH_SHORT_FIELD


def validate_api_response(data):
    pattern = r'^[A-Za-z0-9]+$'

    if data is None:
        raise ApiException('Отсутствует тело запроса')

    elif 'url' not in data or not data['url']:
        raise ApiException('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if (re.sub(pattern, '', data['custom_id'])
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