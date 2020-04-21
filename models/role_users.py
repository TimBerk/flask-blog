from shared import db

role_users = db.Table(
    'role_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('role_id', db.Integer(), db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")),
)
