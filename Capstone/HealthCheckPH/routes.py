from flask import Blueprint, render_template, jsonify, request

from database import test_database_connection
from checkup_service import (
    create_patient_checkup,
    perform_measurement,
    get_checkup_results
)


main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/")
def home():
    return render_template("index.html")


@main_routes.route("/api/database/test")
def test_database():
    try:
        test_database_connection()

        return jsonify({
            "success": True,
            "message": "Database connected successfully."
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@main_routes.route("/api/patient/start", methods=["POST"])
def start_patient_checkup():
    data = request.get_json(silent=True) or {}

    response, status_code = create_patient_checkup(data)

    return jsonify(response), status_code


@main_routes.route("/api/measure/<measure_type>", methods=["POST"])
def measure_sensor(measure_type):
    data = request.get_json(silent=True) or {}
    record_id = data.get("checkup_id")

    response, status_code = perform_measurement(record_id, measure_type)

    return jsonify(response), status_code


@main_routes.route("/api/results/<int:record_id>")
def results(record_id):
    response, status_code = get_checkup_results(record_id)

    return jsonify(response), status_code