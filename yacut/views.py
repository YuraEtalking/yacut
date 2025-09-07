from flask import flash, render_template, request
from sqlalchemy.exc import IntegrityError

from . import app, db
from .forms import UrlForm
from .models import URLMap
from .utility import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def add_url():
    form = UrlForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        url_in_db = URLMap.query.filter_by(original=original_link).first()
        if url_in_db is not None:
            flash('"Эта ссылка уже имеет укороченную версию."')
            short_url = request.url_root + url_in_db.short
            return render_template(
                'url_cut.html',
                url={'url_link': url_in_db.original, 'short_url': short_url},
                form=form
            )

        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id(original_link)
        try:
            url = URLMap(
                original=original_link,
                short=custom_id,
            )
            db.session.add(url)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('"Ошибка, попробуйте еще раз."')

        short_url = request.url_root + url.short
        return render_template(
            'url_cut.html',
            url={'url_link': url.original, 'short_url': short_url},
            form=form
        )
    return render_template('url_cut.html', form=form)


# @app.route('/<str:slug>')
# def opinion_view(slug):
#     opinion = URLMap.query.get_or_404(slug)
#     return render_template('opinion.html', opinion=opinion)
# # todo доделай редирект

