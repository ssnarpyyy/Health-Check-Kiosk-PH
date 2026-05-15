import pymysql
from config import DB_CONFIG


def get_db():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG["port"],
        cursorclass=pymysql.cursors.DictCursor
    )


def test_database_connection():
    db = get_db()
    db.close()
    return True


def insert_sensor_data(cursor, record_id, sensor_type, sensor_value):
    cursor.execute("""
        INSERT INTO sensor_data (record_id, sensor_type, sensor_value)
        VALUES (%s, %s, %s)
    """, (record_id, sensor_type, str(sensor_value)))


def insert_system_log(cursor, user_id, activity, system_event):
    cursor.execute("""
        INSERT INTO system_logs (user_id, activity, system_event)
        VALUES (%s, %s, %s)
    """, (user_id, activity, system_event))