from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    board_title = db.Column(db.String(100), default='Project Board')

    # 1 to many (User:Tasks)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'