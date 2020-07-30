import re
from shared import db


def slugify(str):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str).lower()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)

    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Category #{self.id} {self.name}>'
