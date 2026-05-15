let checkupId = null;
let completedSteps = 0;
let patientInfo = {};

function showScreen(screenId) {
  document.querySelectorAll(".screen").forEach(screen => {
    screen.classList.remove("active");
  });

  document.getElementById(screenId).classList.add("active");
}

function clearErrors() {
  const errorIds = [
    "fullNameError",
    "ageError",
    "sexError",
    "contactError",
    "studentIdError"
  ];

  errorIds.forEach(id => {
    document.getElementById(id).textContent = "";
  });

  document.getElementById("formAlert").style.display = "none";
  document.getElementById("formAlert").textContent = "";
}

function showBackendErrors(errors) {
  clearErrors();

  if (errors.full_name) {
    document.getElementById("fullNameError").textContent = errors.full_name;
  }

  if (errors.age) {
    document.getElementById("ageError").textContent = errors.age;
  }

  if (errors.sex) {
    document.getElementById("sexError").textContent = errors.sex;
  }

  if (errors.contact) {
    document.getElementById("contactError").textContent = errors.contact;
  }

  if (errors.student_id) {
    document.getElementById("studentIdError").textContent = errors.student_id;
  }

  const alertBox = document.getElementById("formAlert");
  alertBox.style.display = "block";
  alertBox.textContent = "Please fix the highlighted fields.";
}

function submitPatient() {
  clearErrors();

  patientInfo = {
    full_name: document.getElementById("fullName").value.trim(),
    age: document.getElementById("age").value.trim(),
    sex: document.getElementById("sex").value,
    contact: document.getElementById("contact").value.trim(),
    student_id: document.getElementById("studentId").value.trim()
  };

  fetch("/api/patient/start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(patientInfo)
  })
    .then(async response => {
      const data = await response.json();

      if (!response.ok) {
        showBackendErrors(data.errors || {});
        return;
      }

      checkupId = data.checkup_id;
      resetMeasurements();

      document.getElementById("patientNameLabel").textContent =
        "Patient: " + patientInfo.full_name;

      showScreen("measurementScreen");
    })
    .catch(() => {
      const alertBox = document.getElementById("formAlert");
      alertBox.style.display = "block";
      alertBox.textContent = "Server error. Please check if Flask is running.";
    });
}

function resetMeasurements() {
  completedSteps = 0;

  for (let i = 1; i <= 6; i++) {
    document.getElementById("badge" + i).textContent = "Waiting";
    document.getElementById("badge" + i).className = "badge";
    document.getElementById("value" + i).textContent = "--";

    const card = document.getElementById("step" + i);
    card.classList.remove("active-step");
    card.classList.add("disabled-step");

    const button = document.getElementById("btn" + i);
    button.disabled = true;
    button.textContent = i === 6 ? "Calculate BMI" : "Start Measurement";
  }

  document.getElementById("step1").classList.add("active-step");
  document.getElementById("step1").classList.remove("disabled-step");
  document.getElementById("btn1").disabled = false;

  document.getElementById("viewResultsBtn").disabled = true;
  updateProgress();
}

function updateProgress() {
  document.getElementById("progressText").textContent =
    completedSteps + "/6 completed";

  const percent = (completedSteps / 6) * 100;
  document.getElementById("progressFill").style.width = percent + "%";
}

function measureStep(stepNumber, measureType) {
  const button = document.getElementById("btn" + stepNumber);
  const badge = document.getElementById("badge" + stepNumber);

  button.disabled = true;
  button.textContent = "Measuring...";
  badge.textContent = "Measuring";
  badge.className = "badge measuring";

  fetch("/api/measure/" + measureType, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      checkup_id: checkupId
    })
  })
    .then(async response => {
      const data = await response.json();

      if (!response.ok) {
        alert(data.message || "Measurement failed.");
        button.disabled = false;
        button.textContent = stepNumber === 6 ? "Calculate BMI" : "Start Measurement";
        badge.textContent = "Waiting";
        badge.className = "badge";
        return;
      }

      setTimeout(() => {
        displayMeasuredValue(stepNumber, measureType, data.result);

        badge.textContent = "Done";
        badge.className = "badge done";

        button.textContent = "Completed";

        document.getElementById("step" + stepNumber).classList.remove("active-step");

        completedSteps++;
        updateProgress();

        const nextStep = stepNumber + 1;

        if (nextStep <= 6) {
          const nextCard = document.getElementById("step" + nextStep);
          const nextBtn = document.getElementById("btn" + nextStep);

          nextCard.classList.remove("disabled-step");
          nextCard.classList.add("active-step");
          nextBtn.disabled = false;
        }

        if (completedSteps === 6) {
          document.getElementById("viewResultsBtn").disabled = false;
        }
      }, 700);
    })
    .catch(() => {
      alert("Server error. Please check if Flask is running.");
      button.disabled = false;
      button.textContent = stepNumber === 6 ? "Calculate BMI" : "Start Measurement";
      badge.textContent = "Waiting";
      badge.className = "badge";
    });
}

function displayMeasuredValue(stepNumber, measureType, result) {
  const valueBox = document.getElementById("value" + stepNumber);

  if (measureType === "temperature") {
    valueBox.textContent = result.temperature + " °C";
  }

  if (measureType === "heart_spo2") {
    valueBox.textContent = result.heart_rate + " bpm / " + result.spo2 + "%";
  }

  if (measureType === "blood_pressure") {
    valueBox.textContent = result.blood_pressure + " mmHg";
  }

  if (measureType === "height") {
    valueBox.textContent = result.height + " cm";
  }

  if (measureType === "weight") {
    valueBox.textContent = result.weight + " kg";
  }

  if (measureType === "bmi") {
    valueBox.textContent = result.bmi + " - " + result.bmi_category;
  }
}

function showResults() {
  fetch("/api/results/" + checkupId)
    .then(response => response.json())
    .then(data => {
      const patient = data.patient;
      const vitals = data.vitals;

      document.getElementById("resultPatientName").textContent =
        "Patient: " + patient.full_name;

      document.getElementById("resultPatientDetails").textContent =
        patient.age + " years old • " + patient.sex;

      document.getElementById("resTemperature").textContent =
        vitals.temperature + " °C";

      document.getElementById("resHeartRate").textContent =
        vitals.heart_rate + " bpm";

      document.getElementById("resSpo2").textContent =
        vitals.spo2 + "%";

      document.getElementById("resBloodPressure").textContent =
        vitals.blood_pressure + " mmHg";

      document.getElementById("resHeight").textContent =
        vitals.height + " cm";

      document.getElementById("resWeight").textContent =
        vitals.weight + " kg";

      document.getElementById("resBmi").textContent =
        vitals.bmi + " - " + vitals.bmi_category;

      document.getElementById("resStatus").textContent = data.status;

      const remarksList = document.getElementById("remarksList");
      remarksList.innerHTML = "";

      data.remarks.forEach(remark => {
        const li = document.createElement("li");
        li.textContent = remark;
        remarksList.appendChild(li);
      });

      showScreen("resultsScreen");
    })
    .catch(() => {
      alert("Unable to load results.");
    });
}

function restartSystem() {
  checkupId = null;
  completedSteps = 0;
  patientInfo = {};

  document.getElementById("fullName").value = "";
  document.getElementById("age").value = "";
  document.getElementById("sex").value = "";
  document.getElementById("contact").value = "";
  document.getElementById("studentId").value = "";

  clearErrors();
  resetMeasurements();
  showScreen("landingScreen");
}

function printAndGoHome() {
  window.print();
  // Redirect to home after a short delay to allow print dialog to open
  setTimeout(() => {
    window.location.href = "/";
  }, 1000);
}