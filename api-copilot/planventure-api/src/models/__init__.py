from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .user_utils import hash_password, verify_password

db = SQLAlchemy()

# Import models after db initialization to avoid circular imports
from .trip import Trip

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """Set the user's password hash."""
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return verify_password(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
