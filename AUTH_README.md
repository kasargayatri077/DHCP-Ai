# Authentication System for Diabetes Prediction App

## Overview
This authentication system provides secure user registration, login, and session management for the Diabetes Prediction System using SQLite database.

## Features

### 🔐 User Authentication
- **Sign Up**: New user registration with email validation and password strength requirements
- **Sign In**: Secure login with username/email and password
- **Session Management**: Automatic session creation and validation
- **Logout**: Secure session termination

### 🔒 Security Features
- **Password Hashing**: SHA-256 encryption for all passwords
- **Session Tokens**: Unique session tokens with 24-hour expiration
- **Input Validation**: Email format validation and password strength requirements
- **SQL Injection Protection**: Parameterized queries for database operations

### 👤 User Management
- **Profile Page**: View account information and statistics
- **Password Change**: Secure password update functionality
- **Account Statistics**: Track account creation and last login dates

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### User Sessions Table
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## File Structure

```
├── main.py                 # Main application with auth integration
├── database.py            # Database operations and user management
├── auth/
│   ├── __init__.py        # Auth package initialization
│   ├── auth_manager.py    # Authentication flow management
│   ├── signin.py          # Sign in page
│   └── signup.py          # Sign up page
└── Tabs/
    └── profile.py         # User profile page
```

## Usage

### Running the App
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run main.py`
3. The app will automatically create the SQLite database on first run

### User Flow
1. **First Time Users**: Navigate to "Sign Up" tab to create account
2. **Returning Users**: Use "Sign In" tab with username/email and password
3. **Authenticated Users**: Access all app features including Profile page
4. **Logout**: Use the logout button in the sidebar

## Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

## Security Notes
- This is a demo application with basic security measures
- In production, consider implementing:
  - HTTPS encryption
  - Two-factor authentication
  - Rate limiting
  - Password reset functionality
  - Email verification
  - More robust session management

## Database Location
The SQLite database (`users.db`) is created in the root directory of the application.

## Troubleshooting
- If you encounter import errors, ensure all files are in the correct directory structure
- The database is automatically created on first run
- Session tokens expire after 24 hours for security 