"""Database initialization script for PlanVenture API."""
from datetime import datetime, timedelta, timezone
import click
from flask.cli import with_appcontext
from src.models import db, User
from src.models.trip import Trip

# Initialize the database and create tables if they don't exist.
# This command can be run from the command line using Flask CLI.
# cd "c:\Users\sinad\VS Code\api-copilot\api-copilot\planventure-api" ; $env:PYTHONPATH = "." ; flask init-db ;

def init_db():
    """Initialize the database."""
    db.drop_all()
    db.create_all()
    print("Database tables created successfully!")

def seed_db():
    """Seed the database with initial data."""
    # Create test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        email_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    test_user.set_password("password123")
    db.session.add(test_user)
    
    # Create some sample trips
    current_time = datetime.now(timezone.utc)
    trips = [
        Trip(
            user_id=1,  # Will be assigned to test_user
            title="Weekend in Paris",
            destination="Paris, France",
            latitude=48.8566,
            longitude=2.3522,
            start_date=current_time + timedelta(days=30),
            end_date=current_time + timedelta(days=33),
            itinerary={
                "day1": {
                    "morning": "Visit Eiffel Tower",
                    "afternoon": "Louvre Museum",
                    "evening": "Seine River Cruise"
                },
                "day2": {
                    "morning": "Arc de Triomphe",
                    "afternoon": "Champs-Élysées",
                    "evening": "French Restaurant"
                }
            }
        ),
        Trip(
            user_id=1,  # Will be assigned to test_user
            title="Tokyo Adventure",
            destination="Tokyo, Japan",
            latitude=35.6762,
            longitude=139.6503,
            start_date=current_time + timedelta(days=60),
            end_date=current_time + timedelta(days=67),
            itinerary={
                "day1": {
                    "morning": "Tsukiji Fish Market",
                    "afternoon": "Senso-ji Temple",
                    "evening": "Shibuya Crossing"
                },
                "day2": {
                    "morning": "TeamLab Borderless",
                    "afternoon": "Harajuku Shopping",
                    "evening": "Robot Restaurant"
                }
            }
        )
    ]
    
    db.session.add_all(trips)
    db.session.commit()
    print("Database seeded successfully!")

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seed the database with sample data."""
    seed_db()

def register_commands(app):
    """Register database commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
