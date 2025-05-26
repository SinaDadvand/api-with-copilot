# Planventure API 🚁

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/github-samples/planventure)

A Flask-based REST API backend for the Planventure application, featuring JWT authentication, email verification, and trip management capabilities.

## Features

- 🔐 JWT-based Authentication
- ✉️ Email Verification System
- 🌍 Trip Planning & Management
- 📱 CORS Support for Frontend Integration
- 🔄 Token Refresh Mechanism
- 📝 Database Models with SQLAlchemy
- 🚀 RESTful API Design

## Prerequisites
Before you begin, ensure you have the following:

- A GitHub account - [sign up for FREE](https://github.com)
- Access to GitHub Copilot - [sign up for FREE](https://gh.io/gfb-copilot)!
- A Code Editor - [VS Code](https://code.visualstudio.com/download) is recommended
- API Client (like [Bruno](https://github.com/usebruno/bruno))
- Git - [Download & Install Git](https://git-scm.com/downloads)
- Python 3.8 or higher

## 🚀 Getting Started

### Local Development Setup

1. Clone the repository and navigate to the planventure-api directory:
```sh
cd planventure-api
```

2. Create a virtual environment and activate it:
```sh
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

3. Install the required dependencies:
```sh
pip install -r requirements.txt
```

4. Create an `.env` file based on [.sample.env](/planventure-api/.sample.env):
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///planventure.db
CORS_ORIGINS=http://localhost:3000
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:3000
```

5. Initialize the database:
```sh
$env:PYTHONPATH = "."
flask init-db
flask seed-db  # Optional: adds sample data
```

6. Start the Flask development server:
```sh
flask run
```

## 📚 API Endpoints

### Authentication
- POST /auth/register - Register a new user
- POST /auth/verify-email - Verify user's email
- POST /login - User login (returns JWT tokens)
- POST /refresh-token - Refresh access token

### User Management
- GET /users/me - Get current user profile
- GET /users/{id} - Get user by ID
- POST /users - Create new user

### Trip Management
- GET /my/trips - List user's trips (with pagination)
- GET /trips/{id} - Get trip details
- POST /trips - Create new trip
- PUT /trips/{id} - Update trip
- DELETE /trips/{id} - Delete trip

### System
- GET / - Welcome message
- GET /health - Health check endpoint

## 🔒 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```http
Authorization: Bearer your_access_token_here
```

## 🌐 CORS Configuration

The API is configured to allow requests from your React frontend. By default, it accepts requests from `http://localhost:3000`. To add more origins, update the `CORS_ORIGINS` in your `.env` file:

```env
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## 📦 Database Models

- User: Handles user accounts and authentication
- Trip: Manages trip details including itinerary

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.