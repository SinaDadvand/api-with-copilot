from datetime import datetime
from src.models import db

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    itinerary = db.Column(db.JSON)  # Store itinerary as JSON for flexibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with User model
    user = db.relationship('User', backref=db.backref('trips', lazy=True))

    def __repr__(self):
        return f'<Trip {self.title} to {self.destination}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'destination': self.destination,
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'itinerary': self.itinerary,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
