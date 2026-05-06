import re


MEASUREMENT_REQUIREMENTS = {
    "temperature": [],
    "heart_spo2": ["body_temperature"],
    "blood_pressure": ["heart_rate", "spo2"],
    "height": ["blood_pressure"],
    "weight": ["height"],
    "bmi": ["height", "weight"]
}


MEASUREMENT_DISPLAY = {
    "body_temperature": "Body Temperature",
    "heart_rate": "Heart Rate",
    "spo2": "SpO2",
    "blood_pressure": "Blood Pressure",
    "height": "Height",
    "weight": "Weight",
    "bmi": "BMI"
}


def validate_patient(data):
    errors = {}

    full_name = data.get("full_name", "").strip()
    age = data.get("age", "").strip()
    sex = data.get("sex", "").strip()
    contact = data.get("contact", "").strip()
    branch = data.get("branch", "").strip()

    if not full_name:
        errors["full_name"] = "Full name is required."
    elif len(full_name) < 3:
        errors["full_name"] = "Full name must be at least 3 characters."
    elif not re.match(r"^[A-Za-zÑñ .'-]+$", full_name):
        errors["full_name"] = "Full name must contain letters only."

    try:
        age_value = int(age)

        if age_value < 1 or age_value > 120:
            errors["age"] = "Age must be between 1 and 120."
    except ValueError:
        errors["age"] = "Age must be a valid number."

    if sex not in ["Male", "Female"]:
        errors["sex"] = "Please select sex."

    if contact:
        if len(contact) < 5 or len(contact) > 30:
            errors["contact"] = "Contact number or Student ID must be 5 to 30 characters."
        elif not re.match(r"^[A-Za-z0-9 -]+$", contact):
            errors["contact"] = "Contact number or Student ID contains invalid characters."

    if not branch:
        errors["branch"] = "Location or branch is required."
    elif len(branch) < 2:
        errors["branch"] = "Location or branch is too short."
    elif len(branch) > 100:
        errors["branch"] = "Location or branch is too long."

    return errors


def validate_measurement_order(record, measure_type):
    if measure_type not in MEASUREMENT_REQUIREMENTS:
        return False, "Invalid measurement type."

    for field in MEASUREMENT_REQUIREMENTS[measure_type]:
        if record.get(field) is None or record.get(field) == "":
            return False, f"Please complete {MEASUREMENT_DISPLAY[field]} first."

    completed_field = {
        "temperature": "body_temperature",
        "heart_spo2": "heart_rate",
        "blood_pressure": "blood_pressure",
        "height": "height",
        "weight": "weight",
        "bmi": "bmi"
    }.get(measure_type)

    if completed_field and record.get(completed_field) is not None:
        return False, f"{MEASUREMENT_DISPLAY[completed_field]} is already completed."

    return True, "Measurement allowed."


def validate_sensor_result(measure_type, result):
    errors = []

    if measure_type == "temperature":
        temperature = result.get("temperature")

        if temperature < 34 or temperature > 42:
            errors.append("Temperature reading is outside safe sensor range.")

    elif measure_type == "heart_spo2":
        heart_rate = result.get("heart_rate")
        spo2 = result.get("spo2")

        if heart_rate < 40 or heart_rate > 180:
            errors.append("Heart rate reading is outside safe sensor range.")

        if spo2 < 70 or spo2 > 100:
            errors.append("SpO2 reading is outside safe sensor range.")

    elif measure_type == "blood_pressure":
        systolic = result.get("systolic")
        diastolic = result.get("diastolic")

        if systolic < 70 or systolic > 200:
            errors.append("Systolic blood pressure is outside safe sensor range.")

        if diastolic < 40 or diastolic > 130:
            errors.append("Diastolic blood pressure is outside safe sensor range.")

        if systolic <= diastolic:
            errors.append("Systolic value must be higher than diastolic value.")

    elif measure_type == "height":
        height = result.get("height")

        if height < 80 or height > 230:
            errors.append("Height reading is outside expected range.")

    elif measure_type == "weight":
        weight = result.get("weight")

        if weight < 20 or weight > 250:
            errors.append("Weight reading is outside expected range.")

    elif measure_type == "bmi":
        bmi = result.get("bmi")

        if bmi < 10 or bmi > 70:
            errors.append("BMI result is outside expected range.")

    return errors


def validate_complete_results(row):
    missing = []

    required_fields = [
        "body_temperature",
        "heart_rate",
        "spo2",
        "blood_pressure",
        "height",
        "weight",
        "bmi"
    ]

    for field in required_fields:
        if row.get(field) is None or row.get(field) == "":
            missing.append(MEASUREMENT_DISPLAY[field])

    return missing