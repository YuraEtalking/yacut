"""Вспомогательные функции."""

import hashlib
import secrets

from flask import request
from sqlalchemy import select, exists

from . import db
from .models import URLMap
from .constants import (
    MAX_ATTEMPTS,
    LENGTH_GENERATED_SHORTCODE,
    SALT_SIZE_BYTES
)


def get_unique_short_id(original_link):
    """Генерирует уникальный шорткод для заданной ссылки."""
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        salt = secrets.token_bytes(SALT_SIZE_BYTES)
        attempt += 1
        shortcode = hashlib.sha256(
            original_link.encode("utf-8") + salt
        ).hexdigest()[:LENGTH_GENERATED_SHORTCODE]
        check = select(exists().where(URLMap.short == shortcode))
        if not db.session.execute(check).scalar():
            break
    return shortcode


def build_short_url(shortcode):
    """Строит полный короткий URL на основе текущего домена и шорткода."""
    domain = request.url_root
    return domain + shortcode
