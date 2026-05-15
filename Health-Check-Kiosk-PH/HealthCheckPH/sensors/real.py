class SensorHardwareError(Exception):
    pass


class RealSensorService:
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
        # TODO:
        # Add actual MLX90614 code here.
        # Example future logic:
        # 1. Read object temperature from MLX90614
        # 2. Apply calibration offset
        # 3. Return the same format as simulated sensor
        raise SensorHardwareError("Real MLX90614 temperature sensor is not configured yet.")

    def read_heart_spo2(self):
        # TODO:
        # Add actual MAX30102 code here.
        # Return heart_rate and spo2.
        raise SensorHardwareError("Real MAX30102 heart rate and SpO2 sensor is not configured yet.")

    def read_blood_pressure(self):
        # TODO:
        # Add actual digital blood pressure monitor code here.
        # Usually this may use USB serial or UART.
        raise SensorHardwareError("Real blood pressure monitor is not configured yet.")

    def read_height(self):
        # TODO:
        # Add actual ultrasonic or ToF height sensor code here.
        raise SensorHardwareError("Real height sensor is not configured yet.")

    def read_weight(self):
        # TODO:
        # Add actual load cell + HX711 code here.
        raise SensorHardwareError("Real weight sensor is not configured yet.")

    def calculate_bmi(self, record):
        # Check if measurements are in nested dict (file-based) or top-level (database)
        measurements = record.get("measurements", record) if record else {}
        
        height = measurements.get("height")
        weight = measurements.get("weight")
        
        if not record or height is None or weight is None:
            raise SensorHardwareError("Height and weight are required before calculating BMI.")

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
            "source": "BMI Calculation",
            "calibration_note": "BMI calculated from measured height and weight."
        }