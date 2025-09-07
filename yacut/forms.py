from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import Length, Regexp, Optional, URL

from  .constants import (
    MAX_LENGTH_SHORT_FIELD,
    MAX_LENGTH_ORIGINAL_FIELD,
    MIN_LENGTH_FIELD
)


class UrlForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[URL(
            message='Введите ссылку. '
                    'Ссылка должна начинаться на "https:// и иметь домен."',
            require_tld=True
        ),
        Length(
            MIN_LENGTH_FIELD,
            MAX_LENGTH_ORIGINAL_FIELD,
            message=' Длинна ссылки не может быть менее %(min)d и '
                    'не более %(max)d символов.'
        )]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(
            MIN_LENGTH_FIELD,
            MAX_LENGTH_SHORT_FIELD,
            message=' Длинна короткой ссылки не может быть менее %(min)d и '
                    'не более %(max)d символов.'
        ),
            Optional(),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Допустимы только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')