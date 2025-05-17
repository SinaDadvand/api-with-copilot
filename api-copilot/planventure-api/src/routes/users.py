from flask import Blueprint, jsonify, request
from src.models import db, User
from src.services.jwt_manager import JWTManager
from src.services.auth import token_required
from datetime import datetime
import jwt

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Update last login timestamp
    user.last_login = datetime.now(datetime.timezone.utc)
    db.session.commit()
    
    # Generate tokens
    access_token = JWTManager.generate_token(user)
    refresh_token = JWTManager.generate_refresh_token(user)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@users.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'error': 'Refresh token is required'}), 400
        
    try:
        # Verify refresh token
        if not JWTManager.verify_refresh_token(refresh_token):
            return jsonify({'error': 'Invalid refresh token'}), 401
            
        # Decode token to get user ID
        payload = JWTManager.decode_token(refresh_token)
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 401
            
        # Generate new access token
        new_access_token = JWTManager.generate_token(user)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token'}), 401

@users.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get the current user's profile."""
    return jsonify(current_user.to_dict())
