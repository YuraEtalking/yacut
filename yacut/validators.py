"""Валидация данных API."""

from .constants import MAX_LENGTH_SHORT_FIELD, SHORT_PATTERN, URL_PATTERN
from .error_handlers import ApiException
from .models import URLMap
from .utility import get_unique_short_id


def validate_api_response(data):
    """Валидирует данные запроса и возвращает словарь с original и short."""
    if data is None:
        raise ApiException('Отсутствует тело запроса')

    url = data.get('url')
    if not url:
        raise ApiException('"url" является обязательным полем!')

    if not URL_PATTERN.fullmatch(url):
        raise ApiException('Недопустимое имя для "url"')

    custom_id = data.get('custom_id')

    if custom_id:
        if (not SHORT_PATTERN.fullmatch(custom_id)
                or len(custom_id) > MAX_LENGTH_SHORT_FIELD):
            raise ApiException('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise ApiException(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        custom_id = get_unique_short_id(url)

    return {
        'original': url,
        'short': custom_id,
    }
