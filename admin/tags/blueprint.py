from flask import Blueprint, render_template
from flask import request, flash
from flask import redirect, url_for
from flask_security import login_required

from models.tag import Tag
from .forms import TagForm

from shared import db

tags = Blueprint('tags', __name__)


@tags.route('/')
@login_required
def index():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    tags = Tag.query.order_by(Tag.id.desc())
    pages = tags.paginate(page=page, per_page=10)

    return render_template('tags/index.html', pages=pages)


@tags.route('/create', methods=['POST', 'GET'])
@login_required
def create():

    if request.method == 'POST':

        name = request.form['name']
        color = request.form['color']

        try:
            tag = Tag(name=name, color=color)
            db.session.add(tag)
            db.session.commit()
            return redirect(url_for('tags.index'))
        except Exception as exc:
            db.session.rollback()
            flash(exc.message, 'danger')
            print('Error', exc)

    form = TagForm()
    return render_template('tags/create.html', form=form)


@tags.route('/<id>/edit', methods=['POST', 'GET'])
@login_required
def edit(id):
    tag = Tag.query.filter(Tag.id == id).first()

    if request.method == 'POST':
        form = TagForm(formdata=request.form, obj=tag)
        form.populate_obj(tag)
        db.session.commit()
        return redirect(url_for('tags.index'))

    form = TagForm(obj=tag)
    return render_template('tags/edit.html', tag=tag, form=form)


@tags.route('/<id>/delete')
@login_required
def delete(id):
    Tag.query.filter(Tag.id == id).delete()
    db.session.commit()
    flash('Тэг удален', 'success')
    return redirect(url_for('tags.index'))
