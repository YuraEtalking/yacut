"""Вью-функции сервиса сокращения ссылок."""

from http import HTTPStatus

from flask import abort, flash, redirect, render_template
from flask.typing import ResponseReturnValue

from . import app, db
from .error_handlers import ShortIdAlreadyExistsError
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def shorten_url_view() -> ResponseReturnValue:
    """Обрабатывает форму сокращения URL и отображает результат."""
    form = UrlForm()
    if form.validate_on_submit():
        original_link: str = form.original_link.data
        custom_id: str | None = form.custom_id.data
        try:

            url: URLMap = URLMap.create_or_generate_shortcode({
                'original': original_link,
                'short': custom_id,
            })

        except ShortIdAlreadyExistsError as e:
            flash(str(e), 'error')
            short_url: str = URLMap.build_short_url(custom_id)
            return render_template(
                'url_cut.html',
                url={
                    'original_url': original_link,
                    'short_url': short_url
                },
                form=form
            )
        except Exception:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)

        short_url: str = URLMap.build_short_url(url.short)
        return render_template(
            'url_cut.html',
            url={
                'original_url': url.original,
                'short_url': short_url
            },
            form=form
        )

    return render_template('url_cut.html', form=form)


@app.route('/<string:short_id>')
def follow_short_url(short_id: str) -> ResponseReturnValue:
    """Перенаправляет по оригинальному URL по короткому идентификатору."""
    url: URLMap = URLMap.get_by_short(short_id).first_or_404()
    return redirect(url.original)
