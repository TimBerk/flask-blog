from datetime import datetime
from shared import db


class Comment(db.Model):
    from models import User

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
                        nullable=False)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Comment #{self.id} {self.name}>'
