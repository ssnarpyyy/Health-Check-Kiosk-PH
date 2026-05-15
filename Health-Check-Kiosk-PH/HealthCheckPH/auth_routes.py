from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import login_required, logout_user, login_user
from auth import verify_admin_credentials, get_admin_by_id
from database import get_db


auth_routes = Blueprint("auth_routes", __name__, url_prefix="/admin")


@auth_routes.route("/login", methods=["GET"])
def login_page():
    """Render admin login page"""
    if 'admin_id' in session:
        return redirect(url_for("auth_routes.dashboard"))
    return render_template("admin_login.html")


@auth_routes.route("/login", methods=["POST"])
def login():
    """Handle admin login"""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required"
        }), 400

    admin = verify_admin_credentials(username, password)
    if admin:
        session['admin_id'] = admin.id
        session['admin_username'] = admin.username
        return jsonify({
            "success": True,
            "message": "Login successful",
            "redirect": url_for("auth_routes.dashboard")
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401


@auth_routes.route("/dashboard", methods=["GET"])
def dashboard():
    """Admin dashboard"""
    if 'admin_id' not in session:
        return redirect(url_for("auth_routes.login_page"))
    return render_template("admin_dashboard_simple.html", username=session.get('admin_username'))


@auth_routes.route("/records", methods=["GET"])
def view_records():
    """View patient records page"""
    if 'admin_id' not in session:
        return redirect(url_for("auth_routes.login_page"))
    return render_template("patient_records.html", username=session.get('admin_username'))


@auth_routes.route("/print-logs", methods=["GET"])
def view_print_logs():
    """View print logs page"""
    if 'admin_id' not in session:
        return redirect(url_for("auth_routes.login_page"))
    return render_template("print_logs.html", username=session.get('admin_username'))


@auth_routes.route("/logout", methods=["POST"])
def logout():
    """Handle admin logout"""
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully",
        "redirect": url_for("main_routes.home")
    }), 200


@auth_routes.route("/api/stats", methods=["GET"])
def get_stats():
    """Get health checkup statistics"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        db = get_db()
        with db.cursor() as cursor:
            # Get total checkups
            cursor.execute("SELECT COUNT(*) as total FROM health_records")
            total_checkups = cursor.fetchone()['total']

            # Get today's checkups
            cursor.execute(
                "SELECT COUNT(*) as total FROM health_records WHERE DATE(measurement_datetime) = CURDATE()"
            )
            today_checkups = cursor.fetchone()['total']

            # Get average age
            cursor.execute("SELECT AVG(u.age) as avg_age FROM health_records hr JOIN users u ON hr.user_id = u.user_id")
            avg_age_result = cursor.fetchone()
            avg_age = avg_age_result['avg_age'] if avg_age_result else 0

            # Get gender distribution
            cursor.execute(
                "SELECT u.sex, COUNT(*) as count FROM health_records hr JOIN users u ON hr.user_id = u.user_id GROUP BY u.sex"
            )
            gender_dist = cursor.fetchall()

            db.close()

        return jsonify({
            "success": True,
            "total_checkups": total_checkups,
            "today_checkups": today_checkups,
            "avg_age": round(avg_age, 1) if avg_age else 0,
            "gender_distribution": gender_dist
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@auth_routes.route("/api/records", methods=["GET"])
def get_records():
    """Get patient checkup records with optional search and filter"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        limit = request.args.get("limit", 20, type=int)
        offset = request.args.get("offset", 0, type=int)
        search = request.args.get("search", "").strip()
        gender = request.args.get("gender", "").strip()
        age_range = request.args.get("age", "").strip()

        db = get_db()
        with db.cursor() as cursor:
            # Build the WHERE clause dynamically
            where_clauses = []
            params = []

            # Search by patient name
            if search:
                where_clauses.append("u.full_name LIKE %s")
                params.append(f"%{search}%")

            # Filter by gender
            if gender:
                where_clauses.append("u.sex = %s")
                params.append(gender)

            # Filter by age range
            if age_range == "0-18":
                where_clauses.append("u.age BETWEEN 0 AND 18")
            elif age_range == "19-30":
                where_clauses.append("u.age BETWEEN 19 AND 30")
            elif age_range == "31-50":
                where_clauses.append("u.age BETWEEN 31 AND 50")
            elif age_range == "51-100":
                where_clauses.append("u.age >= 51")

            where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

            query = f"""
                SELECT 
                    hr.record_id,
                    u.full_name as patient_name,
                    u.age,
                    u.sex,
                    hr.body_temperature,
                    hr.heart_rate,
                    hr.spo2,
                    hr.blood_pressure,
                    hr.bmi,
                    hr.status,
                    hr.measurement_datetime as created_at
                FROM health_records hr
                JOIN users u ON hr.user_id = u.user_id
                WHERE {where_clause}
                ORDER BY hr.measurement_datetime DESC
                LIMIT %s OFFSET %s
            """

            params.extend([limit, offset])
            cursor.execute(query, params)
            records = cursor.fetchall()

            # Get total count with filters applied
            count_query = f"""
                SELECT COUNT(*) as total FROM health_records hr
                JOIN users u ON hr.user_id = u.user_id
                WHERE {where_clause}
            """
            count_params = params[:-2]  # Remove LIMIT and OFFSET
            cursor.execute(count_query, count_params)
            total = cursor.fetchone()['total']

            db.close()

        return jsonify({
            "success": True,
            "records": records,
            "total": total,
            "limit": limit,
            "offset": offset
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@auth_routes.route("/api/print-logs", methods=["GET"])
def get_print_logs():
    """Get print logs from system_logs table"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        db = get_db()
        with db.cursor() as cursor:
            # Get all system logs (print activities)
            cursor.execute("""
                SELECT 
                    log_id,
                    user_id,
                    activity,
                    system_event,
                    timestamp
                FROM system_logs
                ORDER BY timestamp DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            logs = cursor.fetchall()

            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM system_logs")
            total = cursor.fetchone()['total']

            db.close()

        return jsonify({
            "success": True,
            "logs": logs,
            "total": total,
            "limit": limit,
            "offset": offset
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


@auth_routes.route("/api/print-patient-record/<int:record_id>", methods=["POST"])
def print_patient_record(record_id):
    """Log a patient record print event"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        db = get_db()
        with db.cursor() as cursor:
            # Get the record
            cursor.execute("""
                SELECT hr.user_id
                FROM health_records hr
                WHERE hr.record_id = %s
            """, (record_id,))
            record = cursor.fetchone()

            if not record:
                return jsonify({
                    "success": False,
                    "message": "Record not found"
                }), 404

            # Log the print event
            cursor.execute("""
                INSERT INTO system_logs (user_id, activity, system_event)
                VALUES (%s, %s, %s)
            """, (
                record['user_id'],
                "Patient record printed",
                f"Record ID {record_id} printed from admin dashboard"
            ))

            db.commit()
            db.close()

        return jsonify({
            "success": True,
            "message": "Print event logged successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
