import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DB = "data.db"


def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            response TEXT NOT NULL,
            FOREIGN KEY(request_id) REFERENCES requests(id)
        )
    """)

    con.commit()
    con.close()


@app.route("/")
def index():
    return jsonify({
        "status": "ok"
    })


@app.route("/admin", methods=["POST"])
def admin():
    data = request.get_json(silent=True)

    if not data or "command" not in data:
        return jsonify({
            "error": "command is required"
        }), 400

    command = data["command"]

    allowed_commands = {
        "ping",
        "hostname",
        "time"
    }

    if command not in allowed_commands:
        return jsonify({
            "error": "command is not allowed"
        }), 403

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO requests (command) VALUES (?)",
        (command,)
    )

    request_id = cur.lastrowid

    con.commit()
    con.close()

    return jsonify({
        "id": request_id,
        "status": "pending"
    }), 201


@app.route("/commands", methods=["GET"])
def get_command():
    con = get_db()
    cur = con.cursor()

    row = cur.execute("""
        SELECT id, command
        FROM requests
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT 1
    """).fetchone()

    con.close()

    if row is None:
        return jsonify({
            "command": None
        })

    return jsonify({
        "id": row["id"],
        "command": row["command"]
    })


@app.route("/response", methods=["POST"])
def response():
    data = request.get_json(silent=True)

    if not data or "request_id" not in data or "response" not in data:
        return jsonify({
            "error": "invalid request"
        }), 400

    request_id = data["request_id"]
    result = data["response"]

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO responses (request_id, response)
        VALUES (?, ?)
    """, (request_id, result))

    cur.execute("""
        UPDATE requests
        SET status = 'completed'
        WHERE id = ?
    """, (request_id,))

    con.commit()
    con.close()

    return jsonify({
        "status": "ok"
    })


@app.route("/responses/<int:request_id>", methods=["GET"])
def get_response(request_id):
    con = get_db()
    cur = con.cursor()

    row = cur.execute("""
        SELECT request_id, response
        FROM responses
        WHERE request_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (request_id,)).fetchone()

    con.close()

    if row is None:
        return jsonify({
            "status": "pending"
        }), 202

    return jsonify({
        "request_id": row["request_id"],
        "response": row["response"]
    })


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
