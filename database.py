import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    # 1. This gets untrusted input from the URL parameter (e.g., /user?id=1)
    user_id = request.args.get("id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 2. VULNERABILITY: String formatting directly inserts user input into the query.
    # CodeQL tracks this untrusted data from the source (request.args) to the sink (execute).
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)

    return str(cursor.fetchall())


if __name__ == "__main__":
    app.run()
