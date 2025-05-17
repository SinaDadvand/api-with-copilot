from datetime import datetime, timezone
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
    password_salt = db.Column(db.String(64), nullable=False)  # Store salt separately
    reset_token_hash = db.Column(db.String(64))  # For password reset functionality
    reset_token_expires = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(64))
    email_verification_sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """Set the user's password hash and salt."""
        password_hash, salt = hash_password(password)
        self.password_hash = password_hash
        self.password_salt = salt

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return verify_password(self.password_hash, password, self.password_salt)
        
    def set_reset_token(self, token: str, expiry: datetime) -> None:
        """Set a password reset token with expiry."""
        from .user_utils import hash_token
        self.reset_token_hash = hash_token(token)
        self.reset_token_expires = expiry

    def verify_reset_token(self, token: str) -> bool:
        """Verify if a reset token is valid and not expired."""
        from .user_utils import hash_token
        if not self.reset_token_hash or not self.reset_token_expires:
            return False
        if datetime.now(datetime.timezone.utc) > self.reset_token_expires:
            return False
        return self.reset_token_hash == hash_token(token)    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
