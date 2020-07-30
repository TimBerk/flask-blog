from flask import Blueprint, render_template
from flask import request, flash
from flask import redirect, url_for
from flask_security import login_required

from models.category import Category
from .forms import CategoryForm

from shared import db

categories = Blueprint('categories', __name__)


@categories.route('/')
@login_required
def index():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    categories = Category.query.order_by(Category.id.desc())
    pages = categories.paginate(page=page, per_page=10)

    return render_template('categories/index.html', pages=pages)


@categories.route('/create', methods=['POST', 'GET'])
@login_required
def create():

    if request.method == 'POST':

        name = request.form['name']
        slug = request.form['slug']

        try:
            category = Category(name=name, slug=slug)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('categories.index'))
        except Exception as exc:
            db.session.rollback()
            flash(exc.message, 'danger')
            print('Error', exc)

    form = CategoryForm()
    return render_template('categories/create.html', form=form)


@categories.route('/<id>/edit', methods=['POST', 'GET'])
@login_required
def edit(id):
    category = Category.query.filter(Category.id == id).first()

    if request.method == 'POST':
        form = CategoryForm(formdata=request.form, obj=category)
        form.populate_obj(category)
        db.session.commit()
        return redirect(url_for('categories.index'))

    form = CategoryForm(obj=category)
    return render_template('categories/edit.html', category=category, form=form)


@categories.route('/<id>/delete')
@login_required
def delete(id):
    Category.query.filter(Category.id == id).delete()
    db.session.commit()
    flash('Категория удалена', 'success')
    return redirect(url_for('categories.index'))
