"""Модуль с моделью SQLAlchemy для оригинальных URL и их коротких кодов."""

from datetime import datetime

from . import db
from .constants import (
    MAX_LENGTH_SHORT_FIELD,
    MAX_LENGTH_ORIGINAL_FIELD
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

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
