# Task 3: Secure Code Assessment

This project demonstrates a manual security code review and vulnerability assessment of a Python application. It includes both a vulnerable version of the code and a remediated, secure version, alongside this assessment report.

## 🎯 Objective
To identify common security weaknesses in application source code, explain their potential impact, and implement secure coding practices to mitigate them. 

## 🛑 Identified Vulnerabilities & Remediation

### 1. Hardcoded Credentials (CWE-798)
* **Location:** `vulnerable_app.py`
* **Vulnerability:** Sensitive information (database username and password) is stored in plain text within the source code.
* **Impact:** If the source code is leaked, the attacker gains immediate access to the database.
* **Fix:** Retrieve secrets from environment variables.

### 2. SQL Injection - SQLi (CWE-89)
* **Location:** `vulnerable_app.py`
* **Vulnerability:** The application uses `f-strings` to concatenate unsanitized user input directly into a SQL query. 
* **Impact:** An attacker can input malicious SQL payloads (e.g., `' OR '1'='1`) to bypass authentication or read hidden data.
* **Fix:** Use Parameterized Queries (Prepared Statements) so the database treats user input strictly as data.

### 3. OS Command Injection (CWE-78)
* **Location:** `vulnerable_app.py`
* **Vulnerability:** `os.system()` is used to execute a system command with unsanitized user input.
* **Impact:** An attacker could input a command separator and a malicious command (e.g., `8.8.8.8 & echo HACKED`).
* **Fix:** Replace `os.system()` with `subprocess.run` and pass arguments as a list.

---

## 🧪 Testing the Code (Proof of Concept)

You can run the included test scripts to see the vulnerabilities being exploited and successfully blocked.

**1. Setup the dummy database:**
```bash
python setup_db.py
```

**2. Test the Vulnerable Application:**
```bash
python test_vulnerable.py
```
*Observe how the SQL Injection successfully returns data, and the Command Injection successfully prints the injected payload to the terminal.*

**3. Test the Secure Application:**
```bash
python test_secure.py
```
*Observe how the SQL Injection returns an empty list `[]`, and the Command Injection throws a controlled error, preventing execution.*

---

## 🛡️ Key Takeaways & Secure Coding Practices
1. **Never trust user input:** Always sanitize, validate, and parameterize input.
2. **Keep secrets out of code:** Use environment variables or secret managers.
3. **Avoid invoking system shells:** Use safer alternatives like `subprocess.run` instead of `os.system()`.