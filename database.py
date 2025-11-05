import sqlite3
import hashlib
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create user_sessions table for tracking login sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "Username or email already exists"
            
            # Hash password and insert user
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            
            conn.commit()
            conn.close()
            return True, "User registered successfully"
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute(
                "SELECT id, username, email FROM users WHERE (username = ? OR email = ?) AND password_hash = ?",
                (username, username, password_hash)
            )
            
            user = cursor.fetchone()
            if user:
                # Update last login
                cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user[0]))
                conn.commit()
                conn.close()
                return True, {"id": user[0], "username": user[1], "email": user[2]}
            else:
                conn.close()
                return False, "Invalid username/email or password"
                
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def create_session(self, user_id):
        """Create a new session for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate session token
            session_token = hashlib.sha256(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
            
            # Set expiration (24 hours from now)
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute(
                "INSERT INTO user_sessions (user_id, session_token, expires_at) VALUES (?, ?, ?)",
                (user_id, session_token, expires_at.strftime('%Y-%m-%d %H:%M:%S'))
            )
            
            conn.commit()
            conn.close()
            return session_token
            
        except Exception as e:
            print(f"Session creation error: {str(e)}")  # Debug print
            return None
    
    def validate_session(self, session_token):
        """Validate session token and return user info"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current time as string for comparison
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                SELECT u.id, u.username, u.email 
                FROM users u 
                JOIN user_sessions s ON u.id = s.user_id 
                WHERE s.session_token = ? AND s.expires_at > ?
            ''', (session_token, current_time))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            return None
            
        except Exception as e:
            print(f"Session validation error: {str(e)}")  # Debug print
            return None
    
    def delete_session(self, session_token):
        """Delete a session (logout)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM user_sessions WHERE session_token = ?", (session_token,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            return False
    
    def update_password(self, user_id, new_password):
        """Update user password"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
            
            conn.commit()
            conn.close()
            return True, "Password updated successfully"
            
        except Exception as e:
            return False, f"Failed to update password: {str(e)}" 
    
    def update_email(self, user_id, new_email):
        """Update user email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = ? AND id != ?", (new_email, user_id))
            if cursor.fetchone():
                conn.close()
                return False, "Email already exists"
            
            cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
            
            conn.commit()
            conn.close()
            return True, "Email updated successfully"
            
        except Exception as e:
            return False, f"Failed to update email: {str(e)}"
    
    def delete_user(self, user_id):
        """Delete user account and all associated data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete user sessions first (foreign key constraint)
            cursor.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
            
            # Delete user
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            conn.commit()
            conn.close()
            return True, "User deleted successfully"
            
        except Exception as e:
            return False, f"Failed to delete user: {str(e)}"