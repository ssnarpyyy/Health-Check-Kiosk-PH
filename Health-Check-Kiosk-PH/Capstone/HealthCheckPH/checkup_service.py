import uuid

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

    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users 
                (username, password_hash, role, full_name, age, sex, contact, branch)
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

            cursor.execute("""
                INSERT INTO health_records (user_id, status)
                VALUES (%s, %s)
            """, (user_id, "In Progress"))

            record_id = cursor.lastrowid
            qr_code = f"HC-{record_id}-{str(uuid.uuid4())[:8]}"

            cursor.execute("""
                INSERT INTO qr_code_records (record_id, qr_code)
                VALUES (%s, %s)
            """, (record_id, qr_code))

            insert_system_log(
                cursor,
                user_id,
                "Patient check-up started",
                "New patient record created"
            )

        db.commit()

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

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": str(error)
        }, 500

    finally:
        db.close()


def perform_measurement(record_id, measure_type):
    if not record_id:
        return {
            "success": False,
            "message": "Missing checkup session."
        }, 400

    db = get_db()
    sensor_service = get_sensor_service()

    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT hr.*, u.user_id
                FROM health_records hr
                JOIN users u ON hr.user_id = u.user_id
                WHERE hr.record_id = %s
            """, (record_id,))

            record = cursor.fetchone()

            if not record:
                return {
                    "success": False,
                    "message": "Invalid checkup session."
                }, 404

            allowed, message = validate_measurement_order(record, measure_type)

            if not allowed:
                return {
                    "success": False,
                    "message": message
                }, 400

            try:
                result = sensor_service.measure(measure_type, record)
            except SensorHardwareError as error:
                return {
                    "success": False,
                    "message": str(error)
                }, 503

            sensor_errors = validate_sensor_result(measure_type, result)

            if sensor_errors:
                insert_system_log(
                    cursor,
                    record["user_id"],
                    "Sensor validation failed",
                    "; ".join(sensor_errors)
                )

                db.commit()

                return {
                    "success": False,
                    "message": "Sensor validation failed.",
                    "errors": sensor_errors
                }, 422

            save_measurement(cursor, record_id, measure_type, result)

            insert_system_log(
                cursor,
                record["user_id"],
                f"{measure_type} measured",
                "Measurement saved successfully"
            )

        db.commit()

        return {
            "success": True,
            "measure_type": measure_type,
            "result": result
        }, 200

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": str(error)
        }, 500

    finally:
        db.close()


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
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    hr.*,
                    u.full_name,
                    u.age,
                    u.sex,
                    u.contact,
                    u.branch,
                    q.qr_code
                FROM health_records hr
                JOIN users u ON hr.user_id = u.user_id
                LEFT JOIN qr_code_records q ON hr.record_id = q.record_id
                WHERE hr.record_id = %s
            """, (record_id,))

            row = cursor.fetchone()

            if not row:
                return {
                    "success": False,
                    "message": "Checkup not found."
                }, 404

            missing_results = validate_complete_results(row)

            if missing_results:
                return {
                    "success": False,
                    "message": "Health check-up is not yet complete.",
                    "missing": missing_results
                }, 400

            status, remarks = evaluate_status(row)

            cursor.execute("""
                UPDATE health_records
                SET status = %s
                WHERE record_id = %s
            """, (status, record_id))

            insert_system_log(
                cursor,
                row["user_id"],
                "Health results viewed",
                "Final health status generated"
            )

        db.commit()

        patient = {
            "full_name": row["full_name"],
            "age": row["age"],
            "sex": row["sex"],
            "contact": row["contact"],
            "branch": row["branch"]
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

        return {
            "success": True,
            "patient": patient,
            "vitals": vitals,
            "status": status,
            "remarks": remarks,
            "qr_code": row["qr_code"],
            "created_at": str(row["measurement_datetime"])
        }, 200

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": str(error)
        }, 500

    finally:
        db.close()