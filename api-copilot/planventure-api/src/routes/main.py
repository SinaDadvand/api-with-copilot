from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@main.route('/health')
def health_check():
    return jsonify({"status": "healthy"})
