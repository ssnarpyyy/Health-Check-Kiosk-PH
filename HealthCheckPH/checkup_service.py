import uuid
import json
from pathlib import Path

from database import get_db, insert_sensor_data, insert_system_log
from validators import (
    validate_patient,
    validate_measurement_order,
    validate_sensor_result,
    validate_complete_results
)
from status_checker import evaluate_status
from sensors.factory import get_sensor_service
from sensors.real import SensorHardwareError
from patient_file_manager import save_patient_info_to_txt

# In-memory storage for when database is unavailable
_checkup_data = {}
CHECKUP_FILE = Path("data/checkup_data.json")


def _load_checkup_data():
    """Load checkup data from file if it exists"""
    global _checkup_data
    if CHECKUP_FILE.exists():
        try:
            with open(CHECKUP_FILE, "r", encoding="utf-8") as f:
                _checkup_data = json.load(f)
        except:
            _checkup_data = {}


def _save_checkup_data():
    """Save checkup data to file"""
    CHECKUP_FILE.parent.mkdir(exist_ok=True)
    with open(CHECKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(_checkup_data, f, indent=2)


def save_patient_txt_backup(record_id, user_id, qr_code, full_name, age, sex, contact, student_id):
    """
    Saves patient information into a .txt file.
    This is only a backup record. MySQL is still the main database.
    """

    patient_data = {
        "record_id": record_id,
        "user_id": user_id,
        "qr_code": qr_code,
        "full_name": full_name,
        "age": age,
        "sex": sex,
        "contact": contact,
        "student_id": student_id
    }

    return save_patient_info_to_txt(patient_data)


def create_patient_checkup(data):
    errors = validate_patient(data)

    if errors:
        return {
            "success": False,
            "errors": errors
        }, 400

    full_name = data.get("full_name", "").strip()
    age = int(data.get("age"))
    sex = data.get("sex")
    contact = data.get("contact", "").strip()
    student_id = data.get("student_id", "").strip()

    # Try to save to database first
    try:
        db = get_db()
        with db.cursor() as cursor:
            # Insert user
            cursor.execute("""
                INSERT INTO users 
                (username, password_hash, role, full_name, age, sex, contact, student_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                full_name,
                None,
                "patient",
                full_name,
                age,
                sex,
                contact,
                student_id
            ))
            
            user_id = cursor.lastrowid

            # Insert health record
            cursor.execute("""
                INSERT INTO health_records (user_id, status)
                VALUES (%s, %s)
            """, (user_id, "In Progress"))
            
            record_id = cursor.lastrowid

            # Generate QR code
            qr_code = f"HC-{record_id}-{str(uuid.uuid4())[:8]}"
            
            # Insert QR code record
            cursor.execute("""
                INSERT INTO qr_code_records (record_id, qr_code)
                VALUES (%s, %s)
            """, (record_id, qr_code))

        db.commit()
        db.close()

        return {
            "success": True,
            "checkup_id": record_id,
            "user_id": user_id,
            "qr_code": qr_code,
            "txt_file": None,
        }, 200

    except Exception as db_error:
        # Fallback to file-based storage if database is unavailable
        print(f"Database error: {str(db_error)}")
        
        _load_checkup_data()
        
        record_id = len(_checkup_data) + 1
        user_id = record_id
        qr_code = f"HC-{record_id}-{str(uuid.uuid4())[:8]}"

        _checkup_data[str(record_id)] = {
            "record_id": record_id,
            "user_id": user_id,
            "full_name": full_name,
            "age": age,
            "sex": sex,
            "contact": contact,
            "student_id": student_id,
            "qr_code": qr_code,
            "status": "In Progress",
            "measurements": {
                "body_temperature": None,
                "heart_rate": None,
                "spo2": None,
                "blood_pressure": None,
                "height": None,
                "weight": None,
                "bmi": None
            }
        }

        _save_checkup_data()

        txt_file_path = save_patient_txt_backup(
            record_id,
            user_id,
            qr_code,
            full_name,
            age,
            sex,
            contact,
            student_id
        )

        return {
            "success": True,
            "checkup_id": record_id,
            "user_id": user_id,
            "qr_code": qr_code,
            "txt_file": txt_file_path,
            "message": "Patient information saved successfully."
        }, 200


def perform_measurement(record_id, measure_type):
    if not record_id:
        return {
            "success": False,
            "message": "Missing checkup session."
        }, 400

    # First try to load from database
    db = None
    record = None
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT hr.*, u.full_name, u.age, u.sex, u.contact, u.student_id
                FROM health_records hr
                JOIN users u ON hr.user_id = u.user_id
                WHERE hr.record_id = %s
            """, (record_id,))
            row = cursor.fetchone()
            
            if row:
                record = {
                    "record_id": row["record_id"],
                    "user_id": row["user_id"],
                    "full_name": row["full_name"],
                    "age": row["age"],
                    "sex": row["sex"],
                    "contact": row["contact"],
                    "student_id": row["student_id"],
                    "measurements": {
                        "body_temperature": row["body_temperature"],
                        "heart_rate": row["heart_rate"],
                        "spo2": row["spo2"],
                        "blood_pressure": row["blood_pressure"],
                        "height": row["height"],
                        "weight": row["weight"],
                        "bmi": row["bmi"]
                    }
                }
        db.close()
    except Exception as db_error:
        print(f"Database load failed: {str(db_error)}")
        if db:
            db.close()

    # If not found in database, try file-based storage
    if not record:
        _load_checkup_data()
        record = _checkup_data.get(str(record_id))

    if not record:
        return {
            "success": False,
            "message": "Invalid checkup session."
        }, 404

    sensor_service = get_sensor_service()

    try:
        # Check measurement order
        allowed, message = validate_measurement_order(record, measure_type)
        if not allowed:
            return {
                "success": False,
                "message": message
            }, 400

        # Get sensor reading
        try:
            result = sensor_service.measure(measure_type, record)
        except SensorHardwareError as error:
            return {
                "success": False,
                "message": str(error)
            }, 503

        # Validate sensor result
        sensor_errors = validate_sensor_result(measure_type, result)
        if sensor_errors:
            return {
                "success": False,
                "message": "Sensor validation failed.",
                "errors": sensor_errors
            }, 422

        # Update measurement in memory structure
        if measure_type == "temperature":
            record["measurements"]["body_temperature"] = result.get("temperature")
        elif measure_type == "heart_spo2":
            record["measurements"]["heart_rate"] = result.get("heart_rate")
            record["measurements"]["spo2"] = result.get("spo2")
        elif measure_type == "blood_pressure":
            record["measurements"]["blood_pressure"] = result.get("blood_pressure")
        elif measure_type == "height":
            record["measurements"]["height"] = result.get("height")
        elif measure_type == "weight":
            record["measurements"]["weight"] = result.get("weight")
        elif measure_type == "bmi":
            record["measurements"]["bmi"] = result.get("bmi")

        # Save to database
        try:
            db = get_db()
            with db.cursor() as cursor:
                save_measurement(cursor, record_id, measure_type, result)
            db.commit()
            db.close()
        except Exception as db_error:
            print(f"Database measurement save failed: {str(db_error)}")
            if db:
                db.close()
            # Still save to file as backup
            _save_checkup_data()

        return {
            "success": True,
            "measure_type": measure_type,
            "result": result
        }, 200

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }, 500


def save_measurement(cursor, record_id, measure_type, result):
    if measure_type == "temperature":
        cursor.execute("""
            UPDATE health_records
            SET body_temperature = %s
            WHERE record_id = %s
        """, (result["temperature"], record_id))

        insert_sensor_data(
            cursor,
            record_id,
            "Temperature Sensor",
            result["temperature"]
        )

    elif measure_type == "heart_spo2":
        cursor.execute("""
            UPDATE health_records
            SET heart_rate = %s, spo2 = %s
            WHERE record_id = %s
        """, (
            result["heart_rate"],
            result["spo2"],
            record_id
        ))

        insert_sensor_data(
            cursor,
            record_id,
            "Heart Rate Sensor",
            result["heart_rate"]
        )

        insert_sensor_data(
            cursor,
            record_id,
            "SpO2 Sensor",
            result["spo2"]
        )

    elif measure_type == "blood_pressure":
        cursor.execute("""
            UPDATE health_records
            SET blood_pressure = %s
            WHERE record_id = %s
        """, (
            result["blood_pressure"],
            record_id
        ))

        insert_sensor_data(
            cursor,
            record_id,
            "Blood Pressure Sensor",
            result["blood_pressure"]
        )

    elif measure_type == "height":
        cursor.execute("""
            UPDATE health_records
            SET height = %s
            WHERE record_id = %s
        """, (
            result["height"],
            record_id
        ))

        insert_sensor_data(
            cursor,
            record_id,
            "Height Sensor",
            result["height"]
        )

    elif measure_type == "weight":
        cursor.execute("""
            UPDATE health_records
            SET weight = %s
            WHERE record_id = %s
        """, (
            result["weight"],
            record_id
        ))

        insert_sensor_data(
            cursor,
            record_id,
            "Weight Sensor",
            result["weight"]
        )

    elif measure_type == "bmi":
        cursor.execute("""
            UPDATE health_records
            SET bmi = %s, bmi_category = %s
            WHERE record_id = %s
        """, (
            result["bmi"],
            result["bmi_category"],
            record_id
        ))

        insert_sensor_data(
            cursor,
            record_id,
            "BMI Calculation",
            f"{result['bmi']} - {result['bmi_category']}"
        )


def get_checkup_results(record_id):
    # Try to load from database first
    db = None
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    hr.*,
                    u.full_name,
                    u.age,
                    u.sex,
                    u.contact,
                    u.student_id,
                    q.qr_code
                FROM health_records hr
                JOIN users u ON hr.user_id = u.user_id
                LEFT JOIN qr_code_records q ON hr.record_id = q.record_id
                WHERE hr.record_id = %s
            """, (record_id,))

            row = cursor.fetchone()

            if row:
                # Check if all measurements are complete
                required_fields = ["body_temperature", "heart_rate", "spo2", "blood_pressure", "height", "weight", "bmi"]
                missing = [f for f in required_fields if row.get(f) is None]
                
                if missing:
                    db.close()
                    return {
                        "success": False,
                        "message": "Health check-up is not yet complete.",
                        "missing": missing
                    }, 400
                
                patient = {
                    "full_name": row["full_name"],
                    "age": row["age"],
                    "sex": row["sex"],
                    "contact": row["contact"],
                    "student_id": row["student_id"]
                }

                vitals = {
                    "temperature": float(row["body_temperature"]),
                    "heart_rate": row["heart_rate"],
                    "spo2": row["spo2"],
                    "blood_pressure": row["blood_pressure"],
                    "height": float(row["height"]),
                    "weight": float(row["weight"]),
                    "bmi": float(row["bmi"]),
                    "bmi_category": row["bmi_category"]
                }

                db.close()
                
                return {
                    "success": True,
                    "patient": patient,
                    "vitals": vitals,
                    "status": row["status"],
                    "remarks": "Health check-up completed successfully.",
                    "qr_code": row["qr_code"],
                    "created_at": str(row["measurement_datetime"])
                }, 200
        
        db.close()
    except Exception as db_error:
        print(f"Database query error: {str(db_error)}")
        if db:
            try:
                db.close()
            except:
                pass

    # Fallback to file-based storage
    _load_checkup_data()
    
    record_id_str = str(record_id)
    
    if record_id_str in _checkup_data:
        record = _checkup_data[record_id_str]
        
        # Check if all measurements are complete
        measurements = record.get("measurements", {})
        required_fields = ["body_temperature", "heart_rate", "spo2", "blood_pressure", "height", "weight", "bmi"]
        missing = [f for f in required_fields if measurements.get(f) is None]
        
        if missing:
            return {
                "success": False,
                "message": "Health check-up is not yet complete.",
                "missing": missing
            }, 400
        
        patient = {
            "full_name": record.get("full_name"),
            "age": record.get("age"),
            "sex": record.get("sex"),
            "contact": record.get("contact"),
            "student_id": record.get("student_id")
        }
        
        vitals = {
            "temperature": measurements.get("body_temperature"),
            "heart_rate": measurements.get("heart_rate"),
            "spo2": measurements.get("spo2"),
            "blood_pressure": measurements.get("blood_pressure"),
            "height": measurements.get("height"),
            "weight": measurements.get("weight"),
            "bmi": measurements.get("bmi"),
            "bmi_category": measurements.get("bmi_category")
        }
        
        return {
            "success": True,
            "patient": patient,
            "vitals": vitals,
            "status": "Complete",
            "remarks": "Health check-up completed successfully.",
            "created_at": record.get("timestamp", "")
        }, 200

    return {
        "success": False,
        "message": "Checkup not found."
    }, 404
    
    return {
        "success": False,
        "message": "Checkup not found."
    }, 404