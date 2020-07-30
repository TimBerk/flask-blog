from flask import Blueprint, render_template
from flask_security import login_required, roles_required

from models.post import Post
from models.user import User
from models.tag import Tag
from models.comments import Comment


admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/')
@login_required
@roles_required('admin')
def index():
    last_posts = Post.query.order_by(Post.created_at.desc()).all()
    posts_cnt = len(last_posts)
    users_cnt = User.query.count()
    tags_cnt = Tag.query.count()
    coments_cnt = Comment.query.count()

    if len(last_posts) >= 2:
        last_posts = last_posts[:2]

    return render_template(
        'admin/index.html',
        posts=last_posts,
        posts_cnt=posts_cnt,
        users_cnt=users_cnt,
        tags_cnt=tags_cnt,
        coments_cnt=coments_cnt,
    )
