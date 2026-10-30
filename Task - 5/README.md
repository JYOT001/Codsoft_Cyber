# Task 5: Secure File Sharing System

A secure, API-based file-sharing application built with Python and Flask. This project demonstrates core cryptographic and access control principles required for secure file storage and transmission.

## 🎯 Features & Security Implementations

1. **Authentication:** Uses Basic Auth with hashed passwords (`werkzeug.security`) to ensure only registered users can access the system.
2. **File Encryption at Rest:** When a file is uploaded, the application encrypts the file byte-by-byte using **AES Symmetric Encryption** (via the `cryptography.fernet` library) before saving it to the disk. 
3. **Role-Based Access Control (RBAC):** Users are assigned roles (`admin` or `user`). A standard user can only download their own uploaded files. An admin can download any file in the system.
4. **Bonus - Ephemeral URLs:** Users can generate secure, temporary download links using `itsdangerous`. These links bypass authentication but automatically **expire after 60 seconds**, preventing unauthorized long-term sharing.

## 🛠️ Setup & Installation

1. Navigate to the Task 5 directory in your terminal:
   ```bash
   cd Codsoft_Cyber/"Task - 5"
   ```
2. Install the required tools:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 How to Run and Test the Application

To test this program, you will act as both the **Server** (hosting the application) and the **User** (uploading/downloading files). You will need two terminal windows open at the same time.

### Step 1: Start the Server
Open your first terminal inside the `Task - 5` folder and run:
```bash
python app.py
```
*Leave this terminal window open. It will create the database, the `secure_uploads` folder, and start listening for requests.*

### Step 2: Prepare the Test File
Open a **second** terminal window, navigate to the `Task - 5` folder, and create a quick test file:
```bash
echo "This is my top secret file for testing!" > secret_data.txt
```

### Step 3: Run the Automated Test
In that same **second** terminal window, run the testing script:
```bash
python test_api.py
```

### What to Observe:
* **In Terminal 1 (The Server):** You will see logs of a user connecting, uploading a file, and downloading it.
* **In Terminal 2 (The User):** You will see the step-by-step results of the test, proving that:
  1. The file was successfully uploaded.
  2. The authorized user could download and decrypt it.
  3. An unauthorized request was successfully blocked.
  4. The 60-second temporary share link was generated and worked.
* **In your Folders:** If you check the `secure_uploads` folder, you will see your file saved as `secret_data.txt.enc`. If you open it in a text editor, it will be completely unreadable ciphertext because it was encrypted by AES.