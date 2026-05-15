# Admin Login Setup Guide

## Overview
Your HealthCheck PH application now includes a complete admin authentication system with:
- **Admin Login Page** - Secure login interface
- **Admin Dashboard** - View statistics and patient records
- **Session Management** - Secure cookie-based sessions
- **Database Integration** - Password-hashed admin credentials

## Files Added/Modified

### New Files
- `auth.py` - Admin authentication logic and database functions
- `auth_routes.py` - Flask routes for login, dashboard, and logout
- `init_admin.py` - Database initialization script
- `templates/admin_login.html` - Admin login page
- `templates/admin_dashboard.html` - Admin dashboard with stats

### Modified Files
- `requirements.txt` - Added `flask-login` and `werkzeug`
- `app.py` - Integrated Flask-Login and authentication routes
- `config.py` - Added SECRET_KEY configuration
- `templates/index.html` - Added admin login link

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `flask` - Web framework
- `flask-login` - Session and user management
- `werkzeug` - Password hashing utilities
- `pymysql` - MySQL database driver

## Step 2: Initialize the Database

Run the initialization script to create the admin table and an initial admin user:

```bash
python init_admin.py
```

**Default credentials:**
- Username: `admin`
- Password: `admin123`

You'll see output like:
```
HealthCheck PH - Admin Setup
========================================
✓ Admin table created successfully

Creating initial admin user...
✓ Admin user created successfully
  Username: admin
  Password: admin123

⚠️  IMPORTANT: Change this password after your first login!
```

## Step 3: Update Secret Key (Production Only)

For production environments, update the `SECRET_KEY` in `config.py` with a strong random string:

```python
# config.py
SECRET_KEY = "your-random-secret-key-here"
```

You can generate one using Python:
```python
import secrets
secrets.token_hex(32)
```

## Step 4: Run Your Application

```bash
python app.py
```

## Accessing the Admin Panel

1. **From the home page**: Click the "Admin Login" link in the top-right corner
2. **Direct URL**: Navigate to `http://localhost:5000/admin/login`

## Admin Dashboard Features

### Login Page (`/admin/login`)
- Secure username and password entry
- Form validation
- Error messaging

### Dashboard (`/admin/dashboard`)
- **Statistics Overview**
  - Total check-ups all-time
  - Today's check-ups
  - Average age of patients
  
- **Recent Check-ups Table**
  - Patient ID, name, age, gender
  - Location/branch
  - Date of check-up
  - Paginated results (10 per page)

### API Endpoints

Available only when logged in:

- `GET /admin/api/stats` - Get dashboard statistics
- `GET /admin/api/records` - Get paginated patient records
  - Parameters: `limit` (default: 20), `offset` (default: 0)

- `POST /admin/logout` - Logout and clear session

## Database Table Structure

The admin table is created automatically:

```sql
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

Passwords are hashed using `werkzeug.security.generate_password_hash` (Werkzeug's PBKDF2 with SHA256).

## Creating Additional Admin Users

### Method 1: Using Python Script

Create a new Python script:

```python
from auth import create_admin

create_admin(
    username="newadmin",
    email="newadmin@healthcheck.ph",
    password="strong_password_here"
)
print("Admin user created!")
```

### Method 2: Direct Database Insert

```python
import pymysql
from werkzeug.security import generate_password_hash
from config import DB_CONFIG

db = pymysql.connect(**DB_CONFIG)
cursor = db.cursor()

password_hash = generate_password_hash("your_password")
cursor.execute(
    "INSERT INTO admins (username, email, password_hash) VALUES (%s, %s, %s)",
    ("username", "email@example.com", password_hash)
)
db.commit()
cursor.close()
db.close()
```

## Security Best Practices

1. **Change Default Password**: After first login, change the default `admin123` password immediately
2. **Use Strong Passwords**: Enforce 8+ characters with mixed case and numbers
3. **Update Secret Key**: Use a strong, random SECRET_KEY in production
4. **HTTPS**: In production, use HTTPS (not HTTP)
5. **Database Backups**: Regularly backup your admin table
6. **Session Management**: Sessions expire based on browser settings

## Troubleshooting

### "Database connection failed"
- Verify MySQL is running
- Check DB_CONFIG in `config.py`
- Ensure `healthcheck_ph` database exists

### "Invalid username or password"
- Verify admin user was created with `init_admin.py`
- Check that username is exactly `admin` (case-sensitive)
- Verify password is `admin123`

### "Module not found: flask_login"
- Run `pip install -r requirements.txt` again
- Verify Flask-Login is installed: `pip show flask-login`

### Admin table doesn't exist
- Run `python init_admin.py` again
- Check database connection and permissions

### Can't logout
- Clear browser cookies manually
- Check browser console for JavaScript errors
- Verify secret key is set in config.py

## File Locations

```
HealthCheckPH/
├── auth.py                    # Authentication logic
├── auth_routes.py             # Admin routes
├── init_admin.py              # Setup script
├── app.py                     # Main app (modified)
├── config.py                  # Config (modified)
├── requirements.txt           # Dependencies (modified)
└── templates/
    ├── admin_login.html       # Login page
    ├── admin_dashboard.html   # Dashboard
    └── index.html             # Home (modified)
```

## Next Steps

- [x] Database table created
- [x] Admin user created
- [x] Authentication routes added
- [x] Dashboard created
- [x] Session management configured
- [ ] Change default password after first login
- [ ] Create additional admin users as needed
- [ ] Set strong SECRET_KEY for production
- [ ] Configure HTTPS in production

## Support

For issues or questions, check:
1. Database connectivity with `/api/database/test`
2. Application logs in terminal
3. Browser console for frontend errors
4. `init_admin.py` output for setup issues
