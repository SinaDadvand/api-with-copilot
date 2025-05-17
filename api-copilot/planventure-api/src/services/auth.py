from functools import wraps
from flask import request, jsonify, current_app
import jwt
from src.models import User
from src.services.jwt_manager import JWTManager

def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route():
            return jsonify({'message': 'This is a protected route'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
            
        try:
            # Decode token
            payload = JWTManager.decode_token(token)
            
            # Verify token type
            if payload.get('type') != 'access':
                return jsonify({'error': 'Invalid token type'}), 401
            
            # Add user to request context
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
    return decorated
