# Planventure - Full Stack Trip Planning Application

A comprehensive trip planning application with a Flask REST API backend and React frontend.

## Project Structure

This repository contains two main components:

- **`planventure-api/`** - Flask-based REST API backend
- **`planventure-client/`** - React frontend application

## Backend Features (Flask API)

- 🔐 JWT Authentication
- 🌍 CORS support for frontend integration
- 📅 Trip planning endpoints
- 🗄️ SQLite database with proper date handling
- 📝 Comprehensive API documentation

## Frontend Features (React Client)

- ⚛️ Modern React application built with Vite
- 🎨 Responsive UI with custom theming
- 🔐 JWT-based authentication flow
- 📱 Trip management interface
- 📅 Itinerary planning components
- 🚀 Fast development with Vite build tool

## Getting Started

### Prerequisites

- **Python 3.8 or higher** (for backend)
- **Node.js 16.0 or higher** (for frontend)
- **npm or yarn** (package managers)
- **pip** (Python package manager)

### Full Stack Setup (Backend + Frontend)

#### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd planventure-api
```

#### Step 2: Backend Setup (Flask API)

1. **Navigate to the API directory:**
```bash
cd planventure-api
```

2. **Create and activate virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the `planventure-api` directory:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

5. **Initialize the database:**
```bash
flask db upgrade
```

6. **Start the Flask development server:**
```bash
flask run
```

The API will be available at `http://localhost:5000`

#### Step 3: Frontend Setup (React Client)

1. **Open a new terminal** and navigate to the client directory:
```bash
cd planventure-client
```

2. **Install Node.js dependencies:**
```bash
npm install
```

3. **Start the React development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Quick Start Commands

After initial setup, use these commands to start both servers:

**Terminal 1 (Backend):**
```bash
cd planventure-api
venv\Scripts\activate  # Windows
flask run
```

**Terminal 2 (Frontend):**
```bash
cd planventure-client
npm run dev
```

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

#### POST /login
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
    "destination": "string"
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
    "destination": "string"
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

## Frontend Development

### Project Structure
The React frontend (`planventure-client/`) includes:

- **Components**: Reusable UI components organized by feature
  - `auth/` - Login and registration forms
  - `trips/` - Trip management components
  - `itinerary/` - Itinerary planning interface
  - `navigation/` - Navigation and layout components
- **Services**: API communication layer
- **Context**: React Context for state management
- **Routes**: Application routing configuration
- **Layouts**: Page layout components

### Development Tools
- **Vite**: Fast build tool and development server
- **ESLint**: Code linting and formatting
- **React Router**: Client-side routing
- **CSS**: Custom styling with responsive design

### Frontend Environment Variables
Create a `.env` file in the `planventure-client` directory:
```env
VITE_API_BASE_URL=http://localhost:5000
```

## Troubleshooting

### Common Issues

#### "vite is not recognized"
If you get this error when trying to run the frontend:
1. Make sure you're in the `planventure-client` directory
2. Run `npm install` to install dependencies
3. Use `npm run dev` instead of `vite` directly

#### CORS Issues
If you get CORS errors:
1. Ensure backend is running on `http://localhost:5000`
2. Ensure frontend is running on `http://localhost:3000`
3. Check the `CORS_ORIGINS` environment variable in backend `.env`

#### Database Issues
If database errors occur:
1. Delete the `instance/planventure.db` file
2. Run `flask db upgrade` again

#### Port Conflicts
If ports are already in use:
- **Backend**: Add `--port 5001` to flask run command
- **Frontend**: Add `--port 3001` to dev command and update CORS_ORIGINS

### Development Workflow
1. Start backend server first: `flask run`
2. Start frontend server: `npm run dev`
3. Open browser to `http://localhost:3000`
4. Backend API accessible at `http://localhost:5000`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
