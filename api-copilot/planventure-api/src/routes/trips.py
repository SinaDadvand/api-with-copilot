from flask import Blueprint, jsonify, request
from src.models import db, Trip
from datetime import datetime

trips = Blueprint('trips', __name__)

@trips.route('/trips', methods=['POST'])
def create_trip():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_id', 'title', 'destination', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Parse dates
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        
        trip = Trip(
            user_id=data['user_id'],
            title=data['title'],
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            itinerary=data.get('itinerary', {})
        )
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify(trip.to_dict()), 201
    
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

@trips.route('/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return jsonify(trip.to_dict())

@trips.route('/users/<int:user_id>/trips', methods=['GET'])
def get_user_trips(user_id):
    trips = Trip.query.filter_by(user_id=user_id).all()
    return jsonify([trip.to_dict() for trip in trips])

@trips.route('/trips/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()
    
    # Update fields if they exist in the request
    if 'title' in data:
        trip.title = data['title']
    if 'destination' in data:
        trip.destination = data['destination']
    if 'start_date' in data:
        trip.start_date = datetime.fromisoformat(data['start_date'])
    if 'end_date' in data:
        trip.end_date = datetime.fromisoformat(data['end_date'])
    if 'latitude' in data:
        trip.latitude = data['latitude']
    if 'longitude' in data:
        trip.longitude = data['longitude']
    if 'itinerary' in data:
        trip.itinerary = data['itinerary']
    
    db.session.commit()
    return jsonify(trip.to_dict())
