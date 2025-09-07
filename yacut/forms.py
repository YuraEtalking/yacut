from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import Length, Optional, URL


class UrlForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[URL(message='Введите ссылку', require_tld=True),
                    Length(1, 1999)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 6), Optional()]
    )
    submit = SubmitField('Создать')