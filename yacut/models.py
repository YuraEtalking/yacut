"""Модуль с моделью SQLAlchemy для оригинальных URL и их коротких кодов."""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime
from typing import Mapping

from flask import request
from sqlalchemy import select, exists
from sqlalchemy.orm import Query

from . import db
from .error_handlers import (
    ShortIdFailedGenerateError,
    ShortIdAlreadyExistsError
)
from .constants import (
    ENCODE,
    MAX_LENGTH_SHORT_FIELD,
    MAX_LENGTH_ORIGINAL_FIELD,
    MAX_ATTEMPTS,
    LENGTH_GENERATED_SHORTCODE,
    SALT_SIZE_BYTES
)


class URLMap(db.Model):
    """Модель сопоставления оригинального URL и его короткого кода."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_FIELD), nullable=False)
    short = db.Column(
        db.String(MAX_LENGTH_SHORT_FIELD),
        unique=True,
        index=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data: Mapping[str, str]) -> None:
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def get_by_short(short_id: str) -> Query[URLMap]:
        """Отдает объект модели по шорткоду."""
        return URLMap.query.filter_by(short=short_id)

    @staticmethod
    def build_short_url(shortcode: str) -> str:
        """Строит полный короткий URL на основе текущего домена и шорткода."""
        domain: str = request.url_root
        return domain + shortcode

    @staticmethod
    def get_unique_short_id(original_link: str) -> str:
        """Генерирует уникальный шорткод для заданной ссылки."""
        attempt = 0
        shortcode: str = ''
        while attempt < MAX_ATTEMPTS:
            salt = secrets.token_bytes(SALT_SIZE_BYTES)
            attempt += 1
            shortcode = hashlib.sha256(
                original_link.encode(ENCODE) + salt
            ).hexdigest()[:LENGTH_GENERATED_SHORTCODE]
            check = select(exists().where(URLMap.short == shortcode))
            if not db.session.execute(check).scalar():
                break
        return shortcode

    @staticmethod
    def create_or_generate_shortcode(data: dict[str, str]) -> URLMap:
        short: str | None = data.get('short')
        original: str | None = data.get('original')

        if not short:
            short = URLMap.get_unique_short_id(original)
            if not short:
                raise ShortIdFailedGenerateError(
                    'Не удалось сгенерировать короткую ссылку.'
                )

        if URLMap.get_by_short(short).first() is not None:
            raise ShortIdAlreadyExistsError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        data['short'] = short
        obj = URLMap()
        obj.from_dict(data)
        db.session.add(obj)
        db.session.commit()
        return obj
