from flask import render_template

from models.post import Post
from app import app


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
