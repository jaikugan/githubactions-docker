from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

@app.route("/api")
def api():
    return jsonify({
        "message": "Hello from Flask Backend",
        "database_host": os.environ.get("DB_HOST")
    })

@app.route("/api/users")
def users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM users")
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify([
            {"id": row[0], "name": row[1]}
            for row in rows
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
