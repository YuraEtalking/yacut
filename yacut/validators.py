"""Валидация данных API."""

from typing import Any, Mapping, Optional

from .constants import MAX_LENGTH_SHORT_FIELD, SHORT_PATTERN, URL_PATTERN
from .error_handlers import ApiException


def validate_api_response(
        data: Optional[Mapping[str, Any]]
) -> dict[str, Optional[str]]:
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
            # Тест требует точно указать именно эту фразу для ошибки.
            raise ApiException('Указано недопустимое имя для короткой ссылки')

    else:
        custom_id = None

    return {
        'original': url,
        'short': custom_id,
    }
