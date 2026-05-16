import pymysql
from config import DB_CONFIG

db = pymysql.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database'],
    port=DB_CONFIG['port'],
    cursorclass=pymysql.cursors.DictCursor
)

with db.cursor() as cursor:
    print('='*120)
    print('PATIENT RECORDS (from users table)')
    print('='*120)
    cursor.execute('SELECT user_id, full_name, age, sex, contact, student_id FROM users ORDER BY user_id')
    for row in cursor.fetchall():
        print(f"ID: {row['user_id']:2} | Name: {row['full_name']:30} | Age: {row['age']:3} | Sex: {row['sex']:6} | Contact: {row['contact']:15} | Student ID: {row['student_id']}")
    
    print('\n' + '='*120)
    print('HEALTH RECORDS WITH MEASUREMENTS')
    print('='*120)
    cursor.execute('''
        SELECT 
            h.record_id,
            u.full_name,
            h.body_temperature,
            h.heart_rate,
            h.spo2,
            h.blood_pressure,
            h.height,
            h.weight,
            h.bmi,
            h.bmi_category,
            h.status,
            h.measurement_datetime
        FROM health_records h
        JOIN users u ON h.user_id = u.user_id
        ORDER BY h.measurement_datetime DESC
        LIMIT 10
    ''')
    for row in cursor.fetchall():
        temp = row['body_temperature'] if row['body_temperature'] else 'N/A'
        hr = row['heart_rate'] if row['heart_rate'] else 'N/A'
        bp = row['blood_pressure'] if row['blood_pressure'] else 'N/A'
        bmi = f"{row['bmi']} ({row['bmi_category']})" if row['bmi'] else 'N/A'
        print(f"Record: {row['record_id']:2} | Patient: {row['full_name']:30} | Temp: {temp} | HR: {hr} | BP: {bp:10} | BMI: {bmi} | Status: {row['status']:12} | Date: {row['measurement_datetime']}")

db.close()
print('\nDatabase view complete!')
