from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional, Dict, Any
from flask import current_app
from src.models import User

class JWTManager:
    @staticmethod
    def generate_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
        """
        Generate a JWT token for a user.
        
        Args:
            user: The User instance to generate token for
            expires_delta: Optional timedelta for token expiration
            
        Returns:
            str: The encoded JWT token
        """
        if expires_delta is None:
            expires_delta = timedelta(days=1)  # Default to 1 day expiration
        payload = {
            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + expires_delta,
            'iat': datetime.now(timezone.utc),
            'type': 'access'  # Add type field for access tokens
        }
        
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def generate_refresh_token(user: User) -> str:
        """
        Generate a refresh token for a user.
        
        Args:
            user: The User instance to generate refresh token for
            
        Returns:
            str: The encoded refresh token
        """
        payload = {            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(days=30),  # 30 days expiration
            'iat': datetime.now(timezone.utc),
            'type': 'refresh'
        }
        
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        
        Args:
            token: The JWT token to decode
            
        Returns:
            dict: The decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid
            jwt.ExpiredSignatureError: If token has expired
        """
        return jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )

    @staticmethod
    def verify_refresh_token(token: str) -> bool:
        """
        Verify if a token is a valid refresh token.
        
        Args:
            token: The token to verify
            
        Returns:
            bool: True if token is a valid refresh token
        """
        try:
            payload = JWTManager.decode_token(token)
            return payload.get('type') == 'refresh'
        except jwt.InvalidTokenError:
            return False
