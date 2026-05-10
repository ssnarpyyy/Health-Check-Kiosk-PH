"""
Database initialization script for admin authentication.
Run this once to set up the admin table and create an initial admin user.
"""

import pymysql
from config import DB_CONFIG
from werkzeug.security import generate_password_hash


def create_admin_table():
    """Create the admins table if it doesn't exist"""
    try:
        db = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        
        with db.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100),
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            db.commit()
            print("✓ Admin table created successfully")
        
        db.close()
        return True
    
    except Exception as error:
        print(f"✗ Error creating admin table: {error}")
        return False


def create_initial_admin(username="admin", password="admin123"):
    """Create an initial admin user"""
    try:
        db = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        
        password_hash = generate_password_hash(password)
        
        with db.cursor() as cursor:
            # Check if admin already exists
            cursor.execute("SELECT id FROM admins WHERE username = %s", (username,))
            if cursor.fetchone():
                print(f"! Admin user '{username}' already exists")
                db.close()
                return False
            
            # Create new admin
            cursor.execute(
                "INSERT INTO admins (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, f"{username}@healthcheck.ph", password_hash)
            )
            db.commit()
            print(f"✓ Admin user created successfully")
            print(f"  Username: {username}")
            print(f"  Password: {password}")
            print(f"\n⚠️  IMPORTANT: Change this password after your first login!")
        
        db.close()
        return True
    
    except Exception as error:
        print(f"✗ Error creating admin user: {error}")
        return False


if __name__ == "__main__":
    print("HealthCheck PH - Admin Setup")
    print("=" * 40)
    
    # Create admin table
    if create_admin_table():
        print("\nCreating initial admin user...")
        create_initial_admin()
        print("\n" + "=" * 40)
        print("Setup completed! You can now login at /admin/login")
    else:
        print("\nSetup failed. Check your database configuration.")
