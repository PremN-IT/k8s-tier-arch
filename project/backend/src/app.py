from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import os

app = Flask(__name__)
CORS(app)

conn = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_NAME']
)
cursor = conn.cursor()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (first_name, middle_name, last_name, username, password, email) VALUES (%s, %s, %s, %s, %s, %s)",
                   (data['first_name'], data['middle_name'], data['last_name'], data['username'], hashed_pw, data['email']))
    conn.commit()
    return jsonify({'msg': 'User registered successfully'})
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor.execute("SELECT password FROM users WHERE username = %s", (data['username'],))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(data['password'].encode('utf-8'), result[0].encode('utf-8')):
        return jsonify({'msg': 'Login successful'})
    return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/')
def home():
    return 'Welcome to the Knowledge Acquisition API'

@app.route('/student', methods=['POST'])
def student():
    data = request.json
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, date_of_joining, fees_paid, department, trainer_name, company_name) VALUES (%s, %s, %s, %s, %s, %s)",
                   (data['name'], data['date_of_joining'], data['fees_paid'], data['department'], data['trainer_name'], data['company_name']))
    conn.commit()
    cursor.close()
    return jsonify({'msg': 'Student data stored'})

@app.route('/students', methods=['GET'])
def get_students():
    cursor =conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")  # Use your actual students table name
    students = cursor.fetchall()
    cursor.close()
    return jsonify(students)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

