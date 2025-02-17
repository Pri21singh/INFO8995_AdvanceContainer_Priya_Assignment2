import logging
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now fetch credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Set up logging
logging.basicConfig(
    filename='app.log',  # Log file will be saved inside the container
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.before_request
def log_request():
    # Log incoming requests
    logging.info(f"Incoming Request: {request.method} {request.url} - Data: {request.get_data()}")

@app.after_request
def log_response(response):
    # Log outgoing responses
    logging.info(f"Outgoing Response: {response.status} - Data: {response.get_data()}")
    return response

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (first_name, last_name) VALUES (%s, %s)", 
                (data["first_name"], data["last_name"]))
    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"id": user_id, "message": "User created successfully"}), 201

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify({"id": user[0], "first_name": user[1], "last_name": user[2]})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
