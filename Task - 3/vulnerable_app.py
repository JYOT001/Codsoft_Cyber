import sqlite3
import os

# VULNERABILITY 1: Hardcoded Credentials
DB_USER = "admin"
DB_PASS = "supersecret123"

def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # VULNERABILITY 2: SQL Injection (SQLi)
    # Directly concatenating user input into the SQL query string
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    return cursor.fetchall()

def ping_server(ip_address):
    # VULNERABILITY 3: OS Command Injection
    # Executing system commands directly with unsanitized user input
    os.system(f"ping -c 1 {ip_address}")