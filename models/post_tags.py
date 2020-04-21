from shared import db


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('posts.id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id', onupdate="CASCADE", ondelete="CASCADE")),
)
