import random
from config import CALIBRATION


def get_temperature_reading():
    raw = round(random.uniform(36.2, 37.1), 2)
    calibrated = round(raw + CALIBRATION["temperature_offset"], 1)

    return {
        "temperature": calibrated,
        "raw_temperature": raw,
        "unit": "°C",
        "calibration_note": "Raw temperature adjusted using calibration offset."
    }


def get_heart_spo2_reading():
    raw_hr = random.randint(72, 98)
    raw_spo2 = random.randint(96, 99)

    heart_rate = raw_hr + CALIBRATION["heart_rate_offset"]
    spo2 = raw_spo2 + CALIBRATION["spo2_offset"]

    return {
        "heart_rate": heart_rate,
        "spo2": spo2,
        "heart_rate_unit": "bpm",
        "spo2_unit": "%",
        "calibration_note": "Pulse sensor values adjusted using calibration offset."
    }


def get_blood_pressure_reading():
    raw_systolic = random.randint(108, 126)
    raw_diastolic = random.randint(70, 84)

    systolic = raw_systolic + CALIBRATION["systolic_offset"]
    diastolic = raw_diastolic + CALIBRATION["diastolic_offset"]

    return {
        "systolic": systolic,
        "diastolic": diastolic,
        "blood_pressure": f"{systolic}/{diastolic}",
        "unit": "mmHg",
        "calibration_note": "Blood pressure reading adjusted using calibration offset."
    }


def get_height_reading():
    raw = round(random.uniform(155, 178), 1)
    calibrated = round(raw + CALIBRATION["height_offset"], 1)

    return {
        "height": calibrated,
        "raw_height": raw,
        "unit": "cm",
        "calibration_note": "Height value adjusted using calibration offset."
    }


def get_weight_reading():
    raw = round(random.uniform(48, 78), 1)
    calibrated = round(raw + CALIBRATION["weight_offset"], 1)

    return {
        "weight": calibrated,
        "raw_weight": raw,
        "unit": "kg",
        "calibration_note": "Weight value adjusted using calibration offset."
    }


def calculate_bmi(height, weight):
    height_m = float(height) / 100
    weight = float(weight)

    bmi = round(weight / (height_m ** 2), 1)

    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"

    return {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "calibration_note": "BMI calculated from calibrated height and weight."
    }