from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db


class Admin(UserMixin):
    def __init__(self, admin_id, username, email):
        self.id = admin_id
        self.username = username
        self.email = email


def get_admin_by_id(admin_id):
    """Retrieve admin by ID from database"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, email FROM admins WHERE id = %s",
                (admin_id,)
            )
            admin_data = cursor.fetchone()
            db.close()

            if admin_data:
                return Admin(
                    admin_data['id'],
                    admin_data['username'],
                    admin_data['email']
                )
    except Exception as error:
        print(f"Error retrieving admin: {error}")
    return None


def verify_admin_credentials(username, password):
    """Verify admin credentials and return admin object if valid"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, email, password_hash FROM admins WHERE username = %s",
                (username,)
            )
            admin_data = cursor.fetchone()
            db.close()

            if admin_data and check_password_hash(admin_data['password_hash'], password):
                return Admin(
                    admin_data['id'],
                    admin_data['username'],
                    admin_data['email']
                )
    except Exception as error:
        print(f"Error verifying credentials: {error}")
    return None


def create_admin(username, email, password):
    """Create a new admin user"""
    try:
        password_hash = generate_password_hash(password)
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO admins (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            db.commit()
            db.close()
        return True
    except Exception as error:
        print(f"Error creating admin: {error}")
        return False


def admin_exists(username):
    """Check if admin with given username exists"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM admins WHERE username = %s",
                (username,)
            )
            result = cursor.fetchone()
            db.close()
            return result is not None
    except Exception as error:
        print(f"Error checking admin: {error}")
    return False
