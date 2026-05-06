from datetime import datetime
from pathlib import Path


DATA_FOLDER = Path("data")
PATIENT_FILE = DATA_FOLDER / "patient_records.txt"


def save_patient_info_to_txt(patient_data):
    """
    Saves patient information into a text file.
    This is only a backup record.
    MySQL is still the main database.
    """

    DATA_FOLDER.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""
========================================
HealthCheck Kiosk PH - Patient Record
========================================
Date and Time : {timestamp}
Record ID     : {patient_data.get("record_id")}
User ID       : {patient_data.get("user_id")}
QR Code       : {patient_data.get("qr_code")}

Full Name     : {patient_data.get("full_name")}
Age           : {patient_data.get("age")}
Sex           : {patient_data.get("sex")}
Contact No.   : {patient_data.get("contact")}
Student ID    : {patient_data.get("student_id")}
========================================

"""

    with open(PATIENT_FILE, "a", encoding="utf-8") as file:
        file.write(content)

    return str(PATIENT_FILE)