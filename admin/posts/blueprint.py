import os

from flask import Blueprint, render_template
from flask import request, flash
from flask import redirect, url_for
from flask_security import login_required, roles_required
from flask_login import current_user


from models import Post
from forms import PostForm, enabled_tags

from shared import db
from app import app

posts = Blueprint('posts', __name__, template_folder='admin/templates')


@posts.route('/')
@login_required
@roles_required('admin')
def index():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts = Post.query.order_by(Post.id.desc())
    pages = posts.paginate(page=page, per_page=5)

    return render_template('admin/posts/index.html', pages=pages)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def create():

    if request.method == 'POST':

        form_post = PostForm(request.form)
        photo = form_post.upload_photo()

        if not photo:
            return redirect(request.url)

        try:
            post = Post(
                title=form_post.title.data, text=form_post.text.data,
                is_published=form_post.is_published.data, tags=form_post.tags.data,
                category=form_post.category.data, photo=photo,
                author=current_user
            )
            db.session.add(post)
            db.session.commit()

            flash('Пост добавлен', 'success')
            return redirect(url_for('posts.index'))
        except Exception as exc:
            db.session.rollback()
            flash(exc.message, 'danger')
            print('Error', exc)

    form = PostForm()
    return render_template('admin/posts/create.html', form=form)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def edit(slug):
    post = Post.query.filter(Post.slug == slug).first()
    form = PostForm(obj=post)

    if request.method == 'POST':

        if form.valid_photo():
            post.photo = form.upload_photo(post.photo)

        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.detail', slug=post.slug))

    return render_template('admin/posts/edit.html', post=post, form=form)


@posts.route('/<id>/delete')
@login_required
@roles_required('admin')
def delete(id):
    post = Post.query.filter(Post.id == id).first()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.photo))
    post.delete()
    flash('Пост удален', 'success')
    return render_template('admin/posts/index.html')


@posts.route('/<slug>')
@login_required
@roles_required('admin')
def detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('admin/posts/detail.html', post=post, tags=enabled_tags)
