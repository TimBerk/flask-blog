from shared import db
from datetime import datetime

from flask_security import UserMixin

from models import Role, role_users


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    login_count = db.Column(db.Integer)
    current_login_ip = db.Column(db.String(255))
    current_login_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    roles = db.relationship('Role', secondary=role_users, backref=db.backref('users', lazy="dynamic"),
                            cascade="save-update, merge, delete")

    def __init__(self, email, password=None, *args, **kwargs):
        super(User, self).__init__(email=email, password=password, *args, **kwargs)

        if not self.username:
            self.username = self.email.split("@")[0]

        if not self.roles:
            user_role = Role.query.filter(Role.name == 'user').first()
            self.roles.append(user_role)

    def __repr__(self):
        return f'<User #{self.id} {self.email}>'
