import hashlib

from sqlalchemy import select, exists

from . import db
from .models import URLMap


def get_unique_short_id(original_link):
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        shortcode = hashlib.sha256(
            original_link.encode("utf-8")
        ).hexdigest()[:6]
        check = select(exists().where(URLMap.short == shortcode))
        if not db.session.execute(check).scalar():
            break
    return shortcode



