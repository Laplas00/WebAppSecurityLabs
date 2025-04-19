import os
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    message = None

    mode = "vulnerable"
    if os.path.exists("/tmp/disable_vuln"):
        mode = "safe"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            if mode == "vulnerable":
                # 💀 УЯЗВИМОСТЬ
                query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                cursor.execute(query)

            else:
                # ✅ Безопасная проверка
                query = "SELECT * FROM users WHERE username = ? AND password = ?"
                cursor.execute(query, (username, password))

            result = cursor.fetchone()
            conn.close()

            if result:
                return render_template("flag.html")
            else:
                message = "❌ Неверный логин или пароль."

        except Exception as e:
            message = f"⚠️ Ошибка: {e}"

    return render_template("login.html", message=message, mode=mode)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
