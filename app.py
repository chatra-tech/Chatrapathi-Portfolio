from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        print("DB ERROR:", e)
        return None

# ✅ AUTO CREATE TABLE
def create_table():
    try:
        conn = get_db_connection()
        if conn is None:
            return

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
        print("Table ready")
    except Exception as e:
        print("TABLE ERROR:", e)

create_table()  # 🔥 IMPORTANT

@app.route('/')
def home():
    return "Backend running"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        name = data.get('name')
        roll = data.get('roll')
        email = data.get('email')

        conn = get_db_connection()
        if conn is None:
            return jsonify({"message": "DB connection failed"}), 500

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (name, roll, email) VALUES (%s, %s, %s)",
            (name, roll, email)
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Saved successfully"})

    except Exception as e:
        print("SUBMIT ERROR:", e)
        return jsonify({"message": str(e)}), 500


@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"message": "DB connection failed"}), 500

        cur = conn.cursor()
        cur.execute("SELECT name, roll, email FROM contacts")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {"name": r[0], "roll": r[1], "email": r[2]} for r in rows
        ])

    except Exception as e:
        print("DATA ERROR:", e)
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
