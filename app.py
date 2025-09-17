from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database connection details
db_config = {
    "host": "mysql-container",  # This is the container name, since they are in the same network
    "user": "root",
    "password": "rootpassword",
    "database": "testdb",
}

@app.route('/')
def index():
    return "Welcome to the Two-Tier Flask App!"

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


