from flask import Blueprint, jsonify, request
from src.models import db, Trip
from src.services.auth import token_required
from datetime import datetime

trips = Blueprint('trips', __name__)

@trips.route('/trips', methods=['POST'])
@token_required
def create_trip(current_user):
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'destination', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Parse dates
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        
        trip = Trip(
            user_id=current_user.id,  # Use the authenticated user's ID
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
@token_required
def get_trip(current_user, trip_id):
    trip = Trip.query.get_or_404(trip_id)
    # Check if the trip belongs to the current user
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    return jsonify(trip.to_dict())

@trips.route('/my/trips', methods=['GET'])
@token_required
def get_user_trips(current_user):
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return jsonify([trip.to_dict() for trip in trips])

@trips.route('/trips/<int:trip_id>', methods=['PUT'])
@token_required
def update_trip(current_user, trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # Check if the trip belongs to the current user
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
        
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
