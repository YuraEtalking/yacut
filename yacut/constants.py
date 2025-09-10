"""Константы для web и api"""

import re


# Модели, формы.
MAX_LENGTH_SHORT_FIELD: int = 16
MAX_LENGTH_ORIGINAL_FIELD: int = 1999
MIN_LENGTH_FIELD: int = 1
ENCODE: str = 'utf-8'

# Константы для utility
MAX_ATTEMPTS: int = 10
LENGTH_GENERATED_SHORTCODE: int = 6
SALT_SIZE_BYTES: int = 3

# Константы для валидаторов.
SHORT_PATTERN: re.Pattern[str] = re.compile(r"[A-Za-z0-9]+", re.ASCII)
# Паттерн валидатора URL из WTForms, что бы соответствовать форме.
URL_PATTERN: re.Pattern[str] = re.compile(
    r"^[a-z]+://"
    r"(?P<host>[^\/\?:]+)"
    r"(?P<port>:[0-9]+)?"
    r"(?P<path>\/.*?)?"
    r"(?P<query>\?.*)?$"
)
