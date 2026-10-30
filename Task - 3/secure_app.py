import sqlite3
import subprocess
import os

# FIX 1: Use Environment Variables for sensitive data
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # FIX 2: Parameterized Queries to prevent SQL Injection
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    return cursor.fetchall()

def ping_server(ip_address):
    # FIX 3: Use subprocess with a list of arguments to prevent Command Injection
    try:
        subprocess.run(["ping", "-c", "1", ip_address], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Failed to ping server.")