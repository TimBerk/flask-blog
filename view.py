from flask import render_template, request
from flask import redirect, url_for
from flask_security import login_required, roles_required
from flask_login import current_user

from forms import UserForm
from models import Post, User
from app import app
from shared import db


@app.route('/')
def index():
    posts = Post.query.filter(Post.is_published == 1).order_by(Post.id.desc()).limit(7).all()

    if len(posts) == 7:
        main_post = posts[0]
        posts = posts[1:]
    elif len(posts) >= 2:
        main_post = posts[0]
        posts = posts[1:]
        posts = posts[1:]
    elif len(posts) == 1:
        main_post = posts[0]
        posts = []
    else:
        main_post = []
        posts = []

    return render_template('app/index.html', main_post=main_post, posts=posts)


@app.route('/policy')
def policy():
    return render_template('app/policy.html')


@app.route('/contacts')
def contacts():
    return render_template('app/contacts.html')


@app.route('/profile')
@login_required
@roles_required('user')
def profile():
    user = User.query.filter(User.id == current_user.id).first()

    if request.method == 'POST':
        form = UserForm(formdata=request.form, obj=user)
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('users.index'))

    form = UserForm(obj=user)
    return render_template('app/profile.html', user=user, form=form)
