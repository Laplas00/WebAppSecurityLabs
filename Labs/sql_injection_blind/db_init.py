import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Демонстрационные юзеры
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecret')")
cursor.execute("INSERT INTO users (username, password) VALUES ('john', '1234')")

conn.commit()
conn.close()
