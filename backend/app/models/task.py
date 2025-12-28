from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='backlog', nullable=False) 
    position = db.Column(db.Integer, default=0)
    
    # New / Updated Fields matching your prototype
    tag = db.Column(db.String(50), default='Feature') 
    priority = db.Column(db.String(20), default='Low') 
    due_date = db.Column(db.String(20), nullable=True) 
    
    # JSON Fields for complex data
    assigned_user_ids = db.Column(db.JSON, default=list) 
    history = db.Column(db.JSON, default=list) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'position': self.position,
            'tag': self.tag,
            'urgency': self.priority, 
            'dueDate': self.due_date,
            'assignedUserIds': self.assigned_user_ids,
            'history': self.history,
            'created_at': self.created_at.isoformat()
        }