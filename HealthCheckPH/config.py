DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "healthcheck_ph",
    "port": 3306
}

# Use "simulated" for prototype.
# Change to "real" once sensors are connected.
SENSOR_MODE = "simulated"

CALIBRATION = {
    "temperature_offset": 0.1,
    "heart_rate_offset": -1,
    "spo2_offset": 0,
    "systolic_offset": 2,
    "diastolic_offset": 1,
    "height_offset": -0.5,
    "weight_offset": 0.2
}

# Secret key for Flask session management
# Change this to a strong random key in production
SECRET_KEY = "your-secret-key-change-in-production"