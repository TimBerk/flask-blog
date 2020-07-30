from flask_security import RoleMixin
from shared import db


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Role #{self.id} {self.name}>'
