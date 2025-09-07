from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import Length, Regexp, Optional, URL


class UrlForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[URL(
            message='Введите ссылку. '
                    'Ссылка должна начинаться на "https:// и иметь домен."',
            require_tld=True
        ),
        Length(
            1,
            1999,
            message=' Длинна ссылки не может быть менее %(min)d и '
                    'не более %(max)d символов.'
        )]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(
            1,
            16,
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