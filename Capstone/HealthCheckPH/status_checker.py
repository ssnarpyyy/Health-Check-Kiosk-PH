def evaluate_status(vitals):
    warnings = []

    temperature = vitals.get("body_temperature")
    heart_rate = vitals.get("heart_rate")
    spo2 = vitals.get("spo2")
    blood_pressure = vitals.get("blood_pressure")
    bmi = vitals.get("bmi")

    if temperature is not None:
        temperature = float(temperature)

        if temperature < 36.0 or temperature > 37.5:
            warnings.append("Temperature is outside normal range.")

    if heart_rate is not None:
        if heart_rate < 60 or heart_rate > 100:
            warnings.append("Heart rate is outside normal range.")

    if spo2 is not None:
        if spo2 < 95:
            warnings.append("SpO2 level is below normal range.")

    if blood_pressure:
        try:
            systolic, diastolic = blood_pressure.split("/")
            systolic = int(systolic)
            diastolic = int(diastolic)

            if systolic >= 140 or diastolic >= 90:
                warnings.append("Blood pressure is high.")
        except ValueError:
            warnings.append("Blood pressure format is invalid.")

    if bmi is not None:
        bmi = float(bmi)

        if bmi < 18.5 or bmi >= 25:
            warnings.append("BMI is outside normal category.")

    if warnings:
        return "Needs Review", warnings

    return "Normal", ["All readings are within normal range."]