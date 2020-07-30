from flask import Blueprint, render_template, flash
from flask import request
from flask import redirect, url_for
from flask_security import login_required, roles_required

from models.user import User
from .forms import UserForm

from shared import db

users = Blueprint('users', __name__)


@users.route('/')
@login_required
@roles_required('admin')
def index():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    users = User.query.order_by(User.created_at.desc())
    pages = users.paginate(page=page, per_page=10)

    return render_template('users/index.html', pages=pages)


@users.route('/create', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def create():

    if request.method == 'POST':

        form_post = UserForm(request.form)
        print(form_post)

        try:
            user = User(
                username=form_post.username.data, email=form_post.email.data,
                password=form_post.password.data, active=form_post.active.data,
                roles=form_post.roles.data
            )
            print(user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.index'))
        except Exception as exc:
            db.session.rollback()
            flash(exc.message, 'danger')
            print('Error', exc)

    form = UserForm()
    return render_template('users/create.html', form=form)


@users.route('/<id>/edit', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def edit(id):
    user = User.query.filter(User.id == id).first()

    if request.method == 'POST':
        form = UserForm(formdata=request.form, obj=user)
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('users.index'))

    form = UserForm(obj=user)
    return render_template('users/edit.html', user=user, form=form)


@users.route('/<id>')
@login_required
def detail(id):
    user = User.query.filter(User.id == id).first()
    return render_template('users/detail.html', user=user)


@users.route('/<id>/delete')
@login_required
@roles_required('admin')
def delete(id):
    user = User.query.filter(User.id == id).first()
    user.delete()
    flash('Пользователь удален', 'success')
    return redirect(url_for('users.index'))
