# Secure Vault

A secure password manager application with encrypted storage, built with FastAPI backend and React TypeScript frontend.

## Overview

This application provides secure password storage with client-server architecture. Users can register accounts, login securely, and manage encrypted password entries through a web interface.

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **SQLite** - Lightweight database for data persistence
- **bcrypt** - Password hashing library
- **cryptography** - AES encryption via Fernet symmetric encryption
- **Pydantic** - Data validation and serialization
- **uvicorn** - ASGI server implementation

### Frontend
- **React 18** - User interface library
- **TypeScript 4.9** - Type-safe JavaScript
- **Axios 1.6** - HTTP client for API communication
- **React Scripts 5.0** - Build tooling and development server
- **CSS3** - Styling and responsive design

## Features

- User registration and authentication
- Secure password storage with AES-256 encryption
- Password entry management (create, read, update, delete)
- Account deletion functionality
- Session-based authentication with tokens
- Responsive web interface
- SQLite database with proper indexing

## Security Implementation

- **Password Hashing**: bcrypt with salt for user passwords
- **Data Encryption**: Fernet (AES-256) for sensitive vault data
- **Key Derivation**: PBKDF2 for master key generation
- **Session Management**: Token-based authentication
- **Database Security**: Foreign key constraints and proper schema design

## Project Structure

```
mini project/
├── api/
│   └── main.py                 # FastAPI application entry point
├── src/
│   ├── auth_manager.py         # User authentication logic
│   ├── crypto_utils.py         # Encryption utilities
│   ├── database_manager_sqlite.py  # Database operations
│   └── vault_manager.py        # Password vault management
├── frontend-react/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API service layer
│   │   └── App.tsx            # Main application component
│   ├── package.json           # Node.js dependencies
│   └── tsconfig.json          # TypeScript configuration
├── tests/                     # Unit tests
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

## Prerequisites

- **Python 3.8+** 
- **Node.js 16+** 
- **npm** (included with Node.js)

## Installation and Setup

### Backend Dependencies

1. Navigate to project directory:
```bash
cd "mini project"
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate     # Windows
# source venv/bin/activate  # macOS/Linux
```

3. Install Python packages:
```bash
pip install --only-binary=all fastapi uvicorn[standard] bcrypt cryptography python-multipart pydantic
```

### Frontend Dependencies

1. Navigate to frontend directory:
```bash
cd frontend-react
```

2. Install Node.js packages:
```bash
npm install
```

## Running the Application

### Step 1: Start the Backend Server

From the project root directory:

```bash
# Navigate to project directory
cd "mini project"

# Activate virtual environment
.\venv\Scripts\activate     # Windows
# source venv/bin/activate  # macOS/Linux

# Navigate to api directory and start server
cd api
python main.py
```

**Backend will be available at:**
- API: http://127.0.0.1:8080
- API Documentation: http://127.0.0.1:8080/docs
- Alternative Docs: http://127.0.0.1:8080/redoc

### Step 2: Start the Frontend Server (New Terminal)

Open a **new terminal** in the project root:

```bash
# Navigate to project directory
cd "mini project"

# Navigate to frontend directory
cd frontend-react

# Start the development server
npm start
```

**Frontend will be available at:**
- Application: http://localhost:3000

## Usage

1. Open http://localhost:3000 in your web browser
2. Register a new account with username and password (minimum 8 characters)
3. Login with your credentials
4. Add password entries for your services
5. Manage your vault entries (view, edit, delete)
6. Access API documentation at http://127.0.0.1:8080/docs

## API Endpoints

### Authentication
- `POST /api/register` - Register new user account
- `POST /api/login` - User login authentication
- `POST /api/logout` - User logout
- `GET /api/check-username/{username}` - Check if username is available

### Vault Management
- `POST /api/vault/entries` - Create new vault entry
- `GET /api/vault/entries` - Retrieve all user vault entries
- `GET /api/vault/entries/{service_name}` - Get specific entry by service name
- `PUT /api/vault/entries/{entry_id}` - Update existing vault entry
- `DELETE /api/vault/entries/{entry_id}` - Delete vault entry

### Account Management
- `DELETE /api/user/delete` - Delete user account and all associated data

## Database Schema

The application uses SQLite with the following main tables:

### Users Table
- Stores user credentials and encryption keys
- Password hashing with bcrypt
- Master key encryption for vault data

### Vault Entries Table
- Stores encrypted password entries
- Foreign key relationship to users
- Timestamps for creation and updates

## Development

### Backend Development
- FastAPI with automatic API documentation
- SQLite database initialization on startup
- Modular architecture with separate managers for auth, crypto, and vault operations

### Frontend Development
- React with TypeScript for type safety
- Axios for API communication with interceptors
- Component-based architecture
- Responsive CSS design

## Security Considerations

- All sensitive data is encrypted before database storage
- User passwords are hashed with bcrypt
- Session tokens for authentication
- CORS configuration for cross-origin requests
- Input validation on both client and server sides
## Testing

Run the test suite:
```bash
cd tests
python test_crypto_utils.py
```

## Troubleshooting

### Common Issues

**Port Already in Use**
- Check if another service is using port 8080 or 3000
- Stop the conflicting service or use different ports

**Module Not Found Errors**
- Ensure virtual environment is activated
- Verify all dependencies are installed with pip install command

**Frontend Compilation Errors**
- Delete node_modules folder and run npm install again
- Clear npm cache with npm cache clean --force

**Database Issues**
- Database file is created automatically on first run
- Check file permissions if database errors occur

### Verification Steps

1. Check Python version: `python --version` (should be 3.8+)
2. Check Node.js version: `node --version` (should be 16+)
3. Backend running: Visit http://127.0.0.1:8080
4. Frontend running: Visit http://localhost:3000

## Notes

- The application creates a SQLite database file automatically on first startup
- All password data is encrypted before storage
- Session tokens are used for authentication
- The frontend uses TypeScript for type safety
- CORS is configured for local development

## Contributing

1. Follow PEP 8 for Python code
2. Use TypeScript strict mode for frontend code
3. Write comprehensive tests for new features
4. Update documentation for API changes


