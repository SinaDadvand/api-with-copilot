from flask import Blueprint, jsonify, request, current_app
from src.models import db, Trip
from src.services.auth import token_required
from datetime import datetime

trips = Blueprint('trips', __name__)

def parse_date_flexible(date_str):
    """Parse date string in either YYYY-MM-DD or ISO format"""
    if 'T' in date_str:
        # ISO format with time
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    else:
        # Date only format - assume start of day
        return datetime.strptime(date_str, '%Y-%m-%d')

def validate_trip_dates(start_date, end_date):
    try:
        start = parse_date_flexible(start_date)
        end = parse_date_flexible(end_date)
            
        if end < start:
            return False, "End date must be after start date"
        return True, None
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD or ISO format"

@trips.route('/trips', methods=['POST'])
@token_required
def create_trip(current_user):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'destination', 'start_date', 'end_date']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Validate field lengths
        if len(data['title'].strip()) < 3:
            return jsonify({'error': 'Trip title must be at least 3 characters long'}), 400
        if len(data['destination'].strip()) < 2:
            return jsonify({'error': 'Destination must be at least 2 characters long'}), 400
        
        # Validate dates
        is_valid, error_msg = validate_trip_dates(data['start_date'], data['end_date'])
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Parse dates flexibly
        start_date = parse_date_flexible(data['start_date'])
        end_date = parse_date_flexible(data['end_date'])
        
        trip = Trip(
            user_id=current_user.id,
            title=data['title'].strip(),
            destination=data['destination'].strip(),
            start_date=start_date,
            end_date=end_date,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            itinerary=data.get('itinerary', {})
        )
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify(trip.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating trip: {str(e)}')
        return jsonify({'error': 'Failed to create trip. Please try again.'}), 500

@trips.route('/trips/<int:trip_id>', methods=['GET'])
@token_required
def get_trip(current_user, trip_id):
    trip = Trip.query.get_or_404(trip_id)
    # Check if the trip belongs to the current user
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    return jsonify(trip.to_dict())

@trips.route('/trips', methods=['GET'])
@token_required
def get_user_trips(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Cap the per_page to prevent performance issues
        per_page = min(per_page, 50)
        
        trips_list = Trip.query.filter_by(user_id=current_user.id)\
            .order_by(Trip.start_date.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'trips': [trip.to_dict() for trip in trips_list.items],
            'total': trips_list.total,
            'pages': trips_list.pages,
            'current_page': trips_list.page,
            'has_next': trips_list.has_next,
            'has_prev': trips_list.has_prev
        })
    except Exception as e:
        current_app.logger.error(f'Error fetching user trips: {str(e)}')
        return jsonify({'error': 'Failed to fetch trips. Please try again.'}), 500

@trips.route('/trips/<int:trip_id>', methods=['PUT'])
@token_required
def update_trip(current_user, trip_id):
    try:
        trip = Trip.query.get_or_404(trip_id)
        
        # Check if the trip belongs to the current user
        if trip.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
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
        
        # Convert date strings to datetime objects if they exist in the data
        if 'start_date' in data:
            data['start_date'] = parse_date_flexible(data['start_date'])
        if 'end_date' in data:
            data['end_date'] = parse_date_flexible(data['end_date'])
            
        # Update fields with validation
        for field in ['title', 'destination', 'start_date', 'end_date', 'latitude', 'longitude', 'itinerary']:
            if field in data:
                if field == 'title' and data[field]:
                    data[field] = data[field].strip()
                    if len(data[field]) < 3:
                        return jsonify({'error': 'Trip title must be at least 3 characters long'}), 400
                elif field == 'destination' and data[field]:
                    data[field] = data[field].strip()
                    if len(data[field]) < 2:
                        return jsonify({'error': 'Destination must be at least 2 characters long'}), 400
                setattr(trip, field, data[field])
        
        db.session.commit()
        
        return jsonify(trip.to_dict())
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating trip: {str(e)}')
        return jsonify({'error': 'Failed to update trip. Please try again.'}), 500

@trips.route('/trips/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_trip(current_user, trip_id):
    try:
        trip = Trip.query.get_or_404(trip_id)
        
        # Check if the trip belongs to the current user
        if trip.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized access'}), 403
            
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({'message': 'Trip deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting trip: {str(e)}')
        return jsonify({'error': 'Failed to delete trip. Please try again.'}), 500
