from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# CREATE TABLE AUTOMATICALLY
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name TEXT,
            roll TEXT,
            email TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

@app.route('/')
def home():
    return "Backend running"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    name = data['name']
    roll = data['roll']
    email = data['email']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, roll, email) VALUES (%s, %s, %s)",
        (name, roll, email)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Saved successfully"})


@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name, roll, email FROM contacts")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"name": r[0], "roll": r[1], "email": r[2]} for r in rows
    ])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
