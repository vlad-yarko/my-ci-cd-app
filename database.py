import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    # 1. This gets untrusted input from the URL parameter (e.g., /user?id=1)
    user_id = request.args.get("id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 2. FIX: Use a parameterized query so user input is bound safely.
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    return str(cursor.fetchall())


if __name__ == "__main__":
    app.run()
