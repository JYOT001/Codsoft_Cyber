import os
import sqlite3
import io
from flask import Flask, request, send_file, jsonify
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-task5-key'
app.config['UPLOAD_FOLDER'] = 'secure_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Symmetric encryption key for AES
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)
link_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def init_db():
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, filename TEXT, encrypted_path TEXT, owner_id INTEGER)''')
    
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('admin', generate_password_hash('admin123'), 'admin'))
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('user1', generate_password_hash('user123'), 'user'))
    conn.commit()
    conn.close()

def authenticate():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return None
    conn = sqlite3.connect('file_sharing.db')
    user = conn.execute("SELECT id, username, password, role FROM users WHERE username=?", (auth.username,)).fetchone()
    conn.close()
    if user and check_password_hash(user[2], auth.password):
        return {'id': user[0], 'username': user[1], 'role': user[3]}
    return None

@app.route('/upload', methods=['POST'])
def upload_file():
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    encrypted_data = cipher.encrypt(file.read())
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".enc")
    with open(save_path, 'wb') as f:
        f.write(encrypted_data)
        
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    c.execute("INSERT INTO files (filename, encrypted_path, owner_id) VALUES (?, ?, ?)", (filename, save_path, user['id']))
    file_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"message": "File encrypted and uploaded!", "file_id": file_id}), 201

@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect('file_sharing.db')
    file_record = conn.execute("SELECT filename, encrypted_path, owner_id FROM files WHERE id=?", (file_id,)).fetchone()
    conn.close()

    if not file_record:
        return jsonify({"error": "File not found"}), 404

    if user['role'] != 'admin' and user['id'] != file_record[2]:
        return jsonify({"error": "Forbidden: RBAC violation."}), 403

    with open(file_record[1], 'rb') as f:
        decrypted_data = cipher.decrypt(f.read())
    return send_file(io.BytesIO(decrypted_data), download_name=file_record[0], as_attachment=True)

@app.route('/share/<int:file_id>', methods=['GET'])
def generate_temp_link(file_id):
    user = authenticate()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect('file_sharing.db')
    file_record = conn.execute("SELECT owner_id FROM files WHERE id=?", (file_id,)).fetchone()
    conn.close()

    if not file_record or (user['role'] != 'admin' and user['id'] != file_record[0]):
        return jsonify({"error": "Forbidden"}), 403

    token = link_serializer.dumps(file_id, salt='file-share-salt')
    return jsonify({"link": request.host_url + f"temp_download/{token}"}), 200

@app.route('/temp_download/<token>', methods=['GET'])
def temp_download(token):
    try:
        file_id = link_serializer.loads(token, salt='file-share-salt', max_age=60)
    except SignatureExpired:
        return jsonify({"error": "Link expired."}), 400
    except Exception:
        return jsonify({"error": "Invalid link."}), 400

    conn = sqlite3.connect('file_sharing.db')
    file_record = conn.execute("SELECT filename, encrypted_path FROM files WHERE id=?", (file_id,)).fetchone()
    conn.close()

    with open(file_record[1], 'rb') as f:
        decrypted_data = cipher.decrypt(f.read())
    return send_file(io.BytesIO(decrypted_data), download_name=file_record[0], as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(port=5000)