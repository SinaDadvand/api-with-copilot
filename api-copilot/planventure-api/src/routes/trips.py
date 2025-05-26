from flask import Blueprint, jsonify, request
from src.models import db, Trip
from src.services.auth import token_required
from datetime import datetime

trips = Blueprint('trips', __name__)

def validate_trip_dates(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end < start:
            return False, "End date must be after start date"
        return True, None
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"

@trips.route('/trips', methods=['POST'])
@token_required
def create_trip(current_user):
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'destination', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate dates
    is_valid, error_msg = validate_trip_dates(data['start_date'], data['end_date'])
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Cap the per_page to prevent performance issues
    per_page = min(per_page, 50)
    
    trips = Trip.query.filter_by(user_id=current_user.id)\
        .order_by(Trip.start_date.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'trips': [trip.to_dict() for trip in trips.items],
        'total': trips.total,
        'pages': trips.pages,
        'current_page': trips.page,
        'has_next': trips.has_next,
        'has_prev': trips.has_prev
    })

@trips.route('/trips/<int:trip_id>', methods=['PUT'])
@token_required
def update_trip(current_user, trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # Check if the trip belongs to the current user
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    # If dates are being updated, validate them
    if 'start_date' in data and 'end_date' in data:
        is_valid, error_msg = validate_trip_dates(data['start_date'], data['end_date'])
        if not is_valid:
            return jsonify({'error': error_msg}), 400
    elif 'start_date' in data:
        is_valid, error_msg = validate_trip_dates(data['start_date'], trip.end_date.strftime('%Y-%m-%d'))
        if not is_valid:
            return jsonify({'error': error_msg}), 400
    elif 'end_date' in data:
        is_valid, error_msg = validate_trip_dates(trip.start_date.strftime('%Y-%m-%d'), data['end_date'])
        if not is_valid:
            return jsonify({'error': error_msg}), 400
    
    try:
        # Convert date strings to datetime objects if they exist in the data
        if 'start_date' in data:
            data['start_date'] = datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            data['end_date'] = datetime.fromisoformat(data['end_date'])
            
        # Update fields
        for field in ['title', 'description', 'start_date', 'end_date', 'location']:
            if field in data:
                setattr(trip, field, data[field])
        
        db.session.commit()
        
        return jsonify(trip.to_dict())
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}), 400

@trips.route('/trips/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_trip(current_user, trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    # Check if the trip belongs to the current user
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
        
    db.session.delete(trip)
    db.session.commit()
    
    return jsonify({'message': 'Trip deleted successfully'}), 200
