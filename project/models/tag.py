from collections import OrderedDict as od
import re

from shared import db


COLORS = [
    (1, 'primary'),
    (2, 'success'),
    (3, 'info'),
    (4, 'warning'),
    (5, 'danger'),
    (6, 'secondary'),
    (7, 'light')
]

DICT_COLORS = od(COLORS)


def slugify(str):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str).lower()


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    color = db.Column(db.Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'

    def get_color(self):
        key_color = list(DICT_COLORS.keys()).index(self.color)
        return COLORS[key_color][1]
