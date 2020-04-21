from shared import db
from datetime import datetime
from flask_login import current_user
import re

from models.post_tags import post_tags
from models.post_comments import post_comments


def slugify(str):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str).lower()


class Post(db.Model):
    from models import User, Category

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(140), nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255), unique=True)
    is_published = db.Column(db.Boolean, nullable=False, default=False, server_default='0')
    user_id = db.Column(db.Integer,
                        db.ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
                        nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey(Category.id, onupdate="CASCADE", ondelete="CASCADE"),
                            nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    published_at = db.Column(db.DateTime, default=datetime.now())

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy="dynamic"))
    comments = db.relationship('Comment', secondary=post_comments, backref=db.backref('post', lazy="dynamic"))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def is_owner(self):
        return self.author == current_user

    def __repr__(self):
        return f'<Post #{self.id} {self.title}>'
