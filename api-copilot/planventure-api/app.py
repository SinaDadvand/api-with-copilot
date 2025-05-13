from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.models import db
from src.routes.main import main
from src.routes.users import users
from src.routes.trips import trips

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(trips)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
