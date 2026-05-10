import random
from config import CALIBRATION


class SimulatedSensorService:
    def measure(self, measure_type, record=None):
        if measure_type == "temperature":
            return self.read_temperature()

        if measure_type == "heart_spo2":
            return self.read_heart_spo2()

        if measure_type == "blood_pressure":
            return self.read_blood_pressure()

        if measure_type == "height":
            return self.read_height()

        if measure_type == "weight":
            return self.read_weight()

        if measure_type == "bmi":
            return self.calculate_bmi(record)

        raise ValueError("Unknown measurement type.")

    def read_temperature(self):
        raw = round(random.uniform(36.2, 37.1), 2)
        calibrated = round(raw + CALIBRATION["temperature_offset"], 1)

        return {
            "temperature": calibrated,
            "raw_temperature": raw,
            "unit": "°C",
            "source": "Simulated MLX90614 Temperature Sensor",
            "calibration_note": "Raw temperature adjusted using calibration offset."
        }

    def read_heart_spo2(self):
        raw_hr = random.randint(72, 98)
        raw_spo2 = random.randint(96, 99)

        heart_rate = raw_hr + CALIBRATION["heart_rate_offset"]
        spo2 = raw_spo2 + CALIBRATION["spo2_offset"]

        return {
            "heart_rate": heart_rate,
            "spo2": spo2,
            "heart_rate_unit": "bpm",
            "spo2_unit": "%",
            "source": "Simulated MAX30102 Heart Rate and SpO2 Sensor",
            "calibration_note": "Pulse sensor values adjusted using calibration offset."
        }

    def read_blood_pressure(self):
        raw_systolic = random.randint(108, 126)
        raw_diastolic = random.randint(70, 84)

        systolic = raw_systolic + CALIBRATION["systolic_offset"]
        diastolic = raw_diastolic + CALIBRATION["diastolic_offset"]

        return {
            "systolic": systolic,
            "diastolic": diastolic,
            "blood_pressure": f"{systolic}/{diastolic}",
            "unit": "mmHg",
            "source": "Simulated Digital Blood Pressure Monitor",
            "calibration_note": "Blood pressure reading adjusted using calibration offset."
        }

    def read_height(self):
        raw = round(random.uniform(155, 178), 1)
        calibrated = round(raw + CALIBRATION["height_offset"], 1)

        return {
            "height": calibrated,
            "raw_height": raw,
            "unit": "cm",
            "source": "Simulated Ultrasonic or ToF Height Sensor",
            "calibration_note": "Height value adjusted using calibration offset."
        }

    def read_weight(self):
        raw = round(random.uniform(48, 78), 1)
        calibrated = round(raw + CALIBRATION["weight_offset"], 1)

        return {
            "weight": calibrated,
            "raw_weight": raw,
            "unit": "kg",
            "source": "Simulated Load Cell and HX711 Weight Sensor",
            "calibration_note": "Weight value adjusted using calibration offset."
        }

    def calculate_bmi(self, record):
        if not record or record.get("height") is None or record.get("weight") is None:
            raise ValueError("Height and weight are required before calculating BMI.")

        height_m = float(record["height"]) / 100
        weight = float(record["weight"])

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
            "source": "BMI Calculation",
            "calibration_note": "BMI calculated from calibrated height and weight."
        }