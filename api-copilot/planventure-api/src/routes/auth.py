from flask import Blueprint, jsonify, request, current_app
from src.models import db, User
from src.services.jwt_manager import JWTManager
from src.services.email_service import send_verification_email
from datetime import datetime, timedelta
import secrets

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Register a new user with email verification."""
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
        email=data['email'],
        email_verified=False,
        email_verification_token=secrets.token_urlsafe(32),
        email_verification_sent_at=datetime.now(datetime.timezone.utc)
    )
    user.set_password(data['password'])
    
    # Save user
    db.session.add(user)
    db.session.commit()
    
    # Send verification email
    try:
        send_verification_email(user.email, user.email_verification_token)
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        # Don't expose the error to the client, but log it
    
    return jsonify({
        'message': 'Registration successful. Please check your email to verify your account.',
        'user': user.to_dict()
    }), 201

@auth.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify user's email address."""
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return jsonify({'error': 'Verification token is required'}), 400
    
    # Find user by verification token
    user = User.query.filter_by(email_verification_token=token).first()
    
    if not user:
        return jsonify({'error': 'Invalid verification token'}), 400
    
    # Check if token has expired (24 hours)
    token_age = datetime.now(datetime.timezone.utc) - user.email_verification_sent_at
    if token_age > timedelta(seconds=current_app.config['EMAIL_VERIFICATION_TIMEOUT']):
        return jsonify({'error': 'Verification token has expired'}), 400
    
    # Mark email as verified
    user.email_verified = True
    user.email_verification_token = None
    user.email_verification_sent_at = None
    db.session.commit()
    
    # Generate tokens for automatic login
    access_token = JWTManager.generate_token(user)
    refresh_token = JWTManager.generate_refresh_token(user)
    
    return jsonify({
        'message': 'Email verification successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email."""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    if user.email_verified:
        return jsonify({'error': 'Email is already verified'}), 400
    
    # Generate new verification token
    user.email_verification_token = secrets.token_urlsafe(32)
    user.email_verification_sent_at = datetime.now(datetime.timezone.utc)
    db.session.commit()
    
    # Send new verification email
    try:
        send_verification_email(user.email, user.email_verification_token)
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        return jsonify({'error': 'Failed to send verification email'}), 500
    
    return jsonify({
        'message': 'Verification email sent successfully'
    }), 200
