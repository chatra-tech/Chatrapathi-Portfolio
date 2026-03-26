from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')
    roll = data.get('roll')
    email = data.get('email')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO contacts (name, roll, email) VALUES (%s, %s, %s)",
            (name, roll, email)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Data saved successfully"})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error saving data"}), 500

@app.route('/')
def home():
    return "Backend running"

if __name__ == '__main__':
    app.run()