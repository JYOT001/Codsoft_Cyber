import secure_app
import os

# Set up dummy environment variables for the test
os.environ["DB_USER"] = "admin"
os.environ["DB_PASS"] = "supersecret123"

print("--- Testing SQL Injection Prevention ---")
payload = "' OR '1'='1"
print(f"Attack Payload ({payload}):", secure_app.get_user_data(payload))

print("\n--- Testing Command Injection Prevention ---")
attack_ip = "8.8.8.8 & echo YOU HAVE BEEN HACKED!"
print(f"Pinging attack IP ({attack_ip}):")
secure_app.ping_server(attack_ip)