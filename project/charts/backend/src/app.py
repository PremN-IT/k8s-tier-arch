from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt
import os
 
app = Flask(__name__)
CORS(app)
 
# All application routes live under /api so the ALB path rule (/api) lines up.
# The ALB does NOT strip the prefix, so Flask must serve the prefixed paths.
api = Blueprint("api", __name__, url_prefix="/api")
 
 
def get_db():
    """New connection per request. RDS closes idle connections, so a single
    long-lived global connection goes stale and every later request fails."""
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        connection_timeout=5,
    )
 
 
# Health check is hit by the ALB directly on the pod IP (:5000/healthz),
# bypassing the ingress path rules. Keep it pure 200 - no DB call - so a
# transient DB blip doesn't mark every target unhealthy and cause a 503 storm.
@app.route("/healthz")
def healthz():
    return "ok", 200
 
 
@app.route("/")
def home():
    return "Welcome to the Knowledge Acquisition API"
 
 
@api.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed_pw = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")  # store as str so it round-trips cleanly from VARCHAR
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, middle_name, last_name, username, password, email) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (data["first_name"], data["middle_name"], data["last_name"],
             data["username"], hashed_pw, data["email"]),
        )
        conn.commit()
        return jsonify({"msg": "User registered successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"msg": "Username already exists"}), 409
    except Error as e:
        return jsonify({"msg": "Database error", "detail": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
 
 
@api.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = %s", (data["username"],)
        )
        result = cursor.fetchone()
        if result and bcrypt.checkpw(
            data["password"].encode("utf-8"), result[0].encode("utf-8")
        ):
            return jsonify({"msg": "Login successful"})
        return jsonify({"msg": "Invalid credentials"}), 401
    except Error as e:
        return jsonify({"msg": "Database error", "detail": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
 
 
@api.route("/student", methods=["POST"])
def student():
    data = request.json
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, date_of_joining, fees_paid, department, trainer_name, company_name) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (data["name"], data["date_of_joining"], data["fees_paid"],
             data["department"], data["trainer_name"], data["company_name"]),
        )
        conn.commit()
        return jsonify({"msg": "Student data stored"})
    except Error as e:
        return jsonify({"msg": "Database error", "detail": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
 
 
@api.route("/students", methods=["GET"])
def get_students():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        return jsonify(cursor.fetchall())
    except Error as e:
        return jsonify({"msg": "Database error", "detail": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
 
 
app.register_blueprint(api)
 
if __name__ == "__main__":
    # Dev only. In the container, run via gunicorn (see Dockerfile).
    app.run(host="0.0.0.0", port=5000)
