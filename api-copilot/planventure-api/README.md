# Planventure API

A Flask-based REST API for trip planning with JWT authentication and CORS support.

## Features

- 🔐 JWT Authentication
- 🌍 CORS support for frontend integration
- 📅 Trip planning endpoints
- 🗄️ SQLite database with proper date handling
- 📝 Comprehensive API documentation

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd planventure-api
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=http://localhost:3000
```

### Running the Application

1. Initialize the database:
```bash
flask db upgrade
```

2. Start the development server:
```bash
flask run
```

The API will be available at `http://localhost:5000`.

## API Documentation

### Authentication Endpoints

#### POST /auth/register
Register a new user.
```json
{
    "username": "string",
    "password": "string",
    "email": "string"
}
```

#### POST /auth/login
Login and receive JWT tokens.
```json
{
    "username": "string",
    "password": "string"
}
```

### Trip Endpoints

All trip endpoints require JWT authentication via the `Authorization` header:
`Authorization: Bearer your-access-token`

#### GET /trips
Get all trips for the authenticated user.

#### GET /trips/{trip_id}
Get a specific trip by ID.

#### POST /trips
Create a new trip.
```json
{
    "title": "string",
    "description": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "location": "string"
}
```

#### PUT /trips/{trip_id}
Update a trip. All fields are optional.
```json
{
    "title": "string",
    "description": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "location": "string"
}
```

#### DELETE /trips/{trip_id}
Delete a trip.

## CORS Configuration

The API is configured to accept requests from specified origins. By default, it accepts requests from `http://localhost:3000`. To add more origins, update the `CORS_ORIGINS` environment variable with comma-separated URLs:

```env
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

The following CORS headers are enabled:
- Access-Control-Allow-Origin
- Access-Control-Allow-Methods (GET, POST, PUT, DELETE, OPTIONS)
- Access-Control-Allow-Headers (Authorization, Content-Type)

## Error Handling

The API returns appropriate HTTP status codes and error messages in JSON format:

```json
{
    "error": "Error message here",
    "status_code": 400
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Token Management

The API uses JWT tokens for authentication with the following features:
- Access tokens include a 'type' field for additional security
- Tokens are signed using HS256 algorithm
- Access tokens expire after 1 hour
- Token validation is handled by a dedicated middleware

## Database

The application uses SQLite as the database backend with proper date handling for trip dates. All dates are stored and returned in ISO format (YYYY-MM-DD).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
