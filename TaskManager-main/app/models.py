from app import db
from datetime import datetime
from enum import Enum, auto

class TaskPriority(str, Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(20), default=TaskPriority.MEDIUM.value)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.name}>'

