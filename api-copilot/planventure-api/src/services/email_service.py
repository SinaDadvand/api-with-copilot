from flask import current_app
from flask_mail import Mail, Message
from threading import Thread

mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)

def send_email(subject: str, recipients: list, html_body: str, text_body: str = None):
    """
    Send an email using Flask-Mail.
    
    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        html_body: HTML content of the email
        text_body: Optional plain text content
    """
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html_body,
        body=text_body or html_body
    )
    
    # Send email asynchronously
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()

def send_verification_email(user_email: str, token: str):
    """Send an email verification link."""    # For development, use direct API URL since we don't have a frontend yet
    verification_url = f"http://127.0.0.1:5000/auth/verify-email?token={token}"
    
    subject = "Verify your PlanVenture account"
    html_body = f"""
    <h1>Welcome to PlanVenture!</h1>
    <p>Thank you for registering. To verify your email address, please click the link below:</p>
    <p><a href="{verification_url}">Verify Email Address</a></p>
    <p>If you did not register for PlanVenture, please ignore this email.</p>
    <p>This link will expire in 24 hours.</p>
    """
    
    send_email(
        subject=subject,
        recipients=[user_email],
        html_body=html_body
    )

def send_password_reset_email(user_email: str, token: str):
    """Send a password reset link."""
    reset_url = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"
    
    subject = "Reset your PlanVenture password"
    html_body = f"""
    <h1>Password Reset Request</h1>
    <p>To reset your password, click the link below:</p>
    <p><a href="{reset_url}">Reset Password</a></p>
    <p>If you did not request a password reset, please ignore this email.</p>
    <p>This link will expire in 1 hour.</p>
    """
    
    send_email(
        subject=subject,
        recipients=[user_email],
        html_body=html_body
    )
