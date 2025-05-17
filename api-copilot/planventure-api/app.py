from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.models import db
from src.models.init_db import register_commands
from src.services.email_service import mail
from src.routes.main import main
from src.routes.users import users
from src.routes.trips import trips
from src.routes.auth import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    mail.init_app(app)
    
    # Register CLI commands
    register_commands(app)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(trips)
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
