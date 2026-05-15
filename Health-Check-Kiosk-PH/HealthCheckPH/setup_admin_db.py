import pymysql
from werkzeug.security import generate_password_hash

# Connect to database
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='healthcheck_ph'
)

cursor = db.cursor()

# Create admins table
cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(100),
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

# Generate password hash for "admin123"
password_hash = generate_password_hash("admin123")

# Insert default admin user
try:
    cursor.execute(
        "INSERT INTO admins (username, email, password_hash) VALUES (%s, %s, %s)",
        ('admin', 'admin@healthcheck.com', password_hash)
    )
    print("✓ Admin user created successfully")
except pymysql.err.IntegrityError:
    print("✓ Admin user already exists")

db.commit()
cursor.close()
db.close()

print("✓ Admins table setup complete!")
print("\nLogin Credentials:")
print("  Username: admin")
print("  Password: admin123")
