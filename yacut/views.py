from http import HTTPStatus
from flask import abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from . import app, db
from .error_handlers import ShortIdGenerationError
from .forms import UrlForm
from .models import URLMap
from .utility import get_unique_short_id, get_short_link



@app.route('/', methods=['GET', 'POST'])
def shorten_url_view():
    form = UrlForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        url_in_db = URLMap.query.filter_by(original=original_link).first()
        if url_in_db is not None:
            flash('"Короткая ссылка для этого адреса уже существует."')
            short_url = get_short_link(url_in_db.short)
            return render_template(
                'url_cut.html',
                url={
                    'original_url': url_in_db.original,
                    'short_url': short_url
                },
                form=form
            )

        custom_id = form.custom_id.data
        try:
            if not custom_id:
                custom_id = get_unique_short_id(original_link)
                if not custom_id:
                    raise ShortIdGenerationError(
                        'Не удалось сгенерировать короткую ссылку.'
                    )

            url = URLMap(original=original_link, short=custom_id)
            db.session.add(url)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('"Этот вариант короткой ссылки уже занят."')
        except Exception:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)

        short_url = get_short_link(url.short)
        return render_template(
            'url_cut.html',
            url={'original_url': url.original, 'short_url': short_url},
            form=form
        )
    return render_template('url_cut.html', form=form)


@app.route('/<string:slug>')
def follow_short_url(slug):
    url = URLMap.query.filter_by(short=slug).first_or_404()
    return redirect(url.original)

