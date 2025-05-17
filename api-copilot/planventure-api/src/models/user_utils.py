from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import hashlib
import base64

SALT_LENGTH = 32  # Length of the salt in bytes
HASH_METHOD = 'pbkdf2:sha256:260000'  # Using PBKDF2 with SHA256 and 260000 iterations

def generate_salt() -> str:
    """Generate a cryptographically secure random salt."""
    return base64.b64encode(secrets.token_bytes(SALT_LENGTH)).decode('utf-8')

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Generate a secure hash of the password using PBKDF2.
    
    Args:
        password: The password to hash
        salt: Optional salt value. If not provided, a new one will be generated
        
    Returns:
        tuple: (password_hash, salt)
    """
    if not salt:
        salt = generate_salt()
    
    salted_password = f"{password}{salt}"
    password_hash = generate_password_hash(salted_password, method=HASH_METHOD)
    
    return password_hash, salt

def verify_password(stored_hash: str, password: str, salt: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        stored_hash: The stored password hash
        password: The password to verify
        salt: The salt used in the original hash
        
    Returns:
        bool: True if password matches, False otherwise
    """
    salted_password = f"{password}{salt}"
    return check_password_hash(stored_hash, salted_password)

def generate_reset_token() -> str:
    """Generate a secure token for password reset."""
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    """
    Create a hash of a token for secure storage.
    Used for password reset tokens, email verification, etc.
    """
    return hashlib.sha256(token.encode()).hexdigest()
