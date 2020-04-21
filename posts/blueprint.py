import os

from flask import Blueprint, render_template
from flask import request, flash
from flask import redirect, url_for
from flask_security import login_required, roles_required
from flask_login import current_user

from models import Post, Comment
from forms import CommentForm, PostForm, enabled_tags

from shared import db
from app import app

user_posts = Blueprint('user_posts', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@user_posts.route('/')
@login_required
def index():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts = Post.query.filter(Post.user_id == current_user.id).order_by(Post.id.desc())
    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/index.html', pages=pages)


@user_posts.route('/category/<slug>')
def category(slug):
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts = Post.query.join(Post.category).filter_by(Post.is_published == 1, slug=slug).order_by(Post.id.desc())
    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/category.html', pages=pages)


@user_posts.route('/tag/<slug>')
def tag(slug):
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts = Post.query.join(Post.tags).filter_by(Post.is_published == 1, slug=slug).order_by(Post.id.desc())
    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/category.html', pages=pages)


@user_posts.route('/create', methods=['POST', 'GET'])
@login_required
@roles_required('user')
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
            return redirect(url_for('user_posts.index'))
        except Exception as exc:
            db.session.rollback()
            flash(exc.message, 'danger')
            print('Error', exc)

    form = PostForm()
    return render_template('posts/create.html', form=form)


@user_posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
@roles_required('user')
def edit(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if not post.is_owner():
        flash('Вы можете редактировать только свои посты', 'danger')
        return redirect(url_for('user_posts.index'))

    form = PostForm(obj=post)

    if request.method == 'POST':

        if form.valid_photo():
            post.photo = form.upload_photo(post.photo)

        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('user_posts.detail', slug=post.slug))

    return render_template('posts/edit.html', post=post, form=form)


@user_posts.route('/<id>/delete')
@login_required
@roles_required('user')
def delete(id):
    post = Post.query.filter(Post.id == id).first()

    if post is None:
        flash('Данный пост не существует', 'danger')
        return redirect(url_for('user_posts.index'))

    if not post.is_owner():
        flash('Вы можете редактировать только свои посты', 'danger')
        return redirect(url_for('user_posts.index'))

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.photo))
    post.delete()
    flash('Пост удален', 'success')
    return render_template('posts/index.html')


@user_posts.route('/<slug>', methods=['POST', 'GET'])
def detail(slug):
    post = Post.query.filter(Post.is_published == 1, Post.slug == slug).first()
    posts = Post.query.filter(Post.slug != slug).order_by(Post.id.desc()).limit(3)

    if request.method == 'POST' and current_user.is_authenticated:

        comment_post = CommentForm(request.form)

        try:
            comment = Comment(
                text=comment_post.text.data
            )
            comment.author = current_user

            db.session.add(comment)
            post.comments.append(comment)
            db.session.add(post)
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            flash(exc.message, 'danger')
            print('Error', exc)

    form = CommentForm()
    return render_template('posts/detail.html', post=post, tags=enabled_tags, posts=posts, form=form)
