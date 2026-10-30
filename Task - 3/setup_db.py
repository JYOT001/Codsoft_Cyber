import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table and add a dummy user
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecret123')")

conn.commit()
conn.close()
print("Dummy database created successfully!")