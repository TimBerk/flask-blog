from shared import db

post_comments = db.Table(
    'post_comments',
    db.Column('post_id', db.Integer(), db.ForeignKey('posts.id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('comment_id', db.Integer(), db.ForeignKey('comments.id', onupdate="CASCADE", ondelete="CASCADE"))
)
