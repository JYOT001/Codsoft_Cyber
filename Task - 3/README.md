# Task 3: Secure Code Assessment

This project demonstrates a manual security code review and vulnerability assessment of a Python application. It includes both a vulnerable version of the code and a remediated, secure version, alongside this assessment report.

## 🎯 Objective
To identify common security weaknesses in application source code, explain their potential impact, and implement secure coding practices to mitigate them. 

## 🛠️ Static Code Analysis
While this assessment was performed manually, these vulnerabilities can also be automatically detected using **Bandit**, a standard static application security testing (SAST) tool for Python. 
*(Running `bandit -r vulnerable_app.py` would successfully flag the hardcoded passwords, SQL injection, and command injection flaws shown below).*

---

## 🛑 Identified Vulnerabilities & Remediation

### 1. Hardcoded Credentials (CWE-798)
* **Location:** Lines 4-6 in `vulnerable_app.py`
* **Vulnerability:** Sensitive information (database username and password) is stored in plain text within the source code.
* **Impact:** If the source code is leaked, committed to a public version control system (like GitHub), or accessed by an unauthorized employee, the attacker gains immediate, unrestricted access to the database.
* **Fix:** Remove hardcoded secrets and retrieve them from environment variables or a secure vault.
  ```python
  # Secure Implementation
  DB_USER = os.environ.get("DB_USER")
  DB_PASS = os.environ.get("DB_PASS")
  ```

### 2. SQL Injection - SQLi (CWE-89)
* **Location:** Line 14 in `vulnerable_app.py`
* **Vulnerability:** The application uses string formatting (`f-strings`) to concatenate unsanitized user input directly into a SQL query. 
* **Impact:** An attacker can input malicious SQL payloads (e.g., `' OR '1'='1`) to bypass authentication, read hidden data, modify records, or drop entire database tables.
* **Fix:** Use Parameterized Queries (Prepared Statements). This ensures the database treats user input strictly as data, never as executable code.
  ```python
  # Secure Implementation
  query = "SELECT * FROM users WHERE username = ?"
  cursor.execute(query, (username,))
  ```

### 3. OS Command Injection (CWE-78)
* **Location:** Line 22 in `vulnerable_app.py`
* **Vulnerability:** The `os.system()` function is used to execute a system ping command with unsanitized user input (`ip_address`).
* **Impact:** An attacker could input an IP address followed by a command separator and a malicious command (e.g., `8.8.8.8; cat /etc/shadow` or `8.8.8.8 & rm -rf /`). The server would execute the attacker's code with the application's privileges.
* **Fix:** Replace `os.system()` with the `subprocess` module and pass arguments as a list. This prevents the shell from interpreting shell metacharacters like `;`, `&`, or `|`.
  ```python
  # Secure Implementation
  subprocess.run(["ping", "-c", "1", ip_address], check=True, capture_output=True, text=True)
  ```

## 🛡️ Key Takeaways & Secure Coding Practices
1. **Never trust user input:** Always sanitize, validate, and parameterize input.
2. **Keep secrets out of code:** Use `.env` files, environment variables, or secret managers (like AWS Secrets Manager or HashiCorp Vault).
3. **Avoid invoking system shells:** Use built-in libraries or safer alternatives (like `subprocess.run` with list arguments) instead of `os.system()` or `os.popen()`.