import requests

BASE_URL = 'http://127.0.0.1:5000'
USER_AUTH = ('user1', 'user123') 

# 1. Create a dummy file to upload
with open('secret_data.txt', 'w') as f:
    f.write("This is highly confidential data for Task 5!")

print("--- 1. Testing Secure File Upload ---")
with open('secret_data.txt', 'rb') as f:
    upload_res = requests.post(f"{BASE_URL}/upload", auth=USER_AUTH, files={'file': f})
print(f"Status: {upload_res.status_code} | {upload_res.json()}")
file_id = upload_res.json().get('file_id')

print("\n--- 2. Testing Secure File Download (Authorized User) ---")
download_res = requests.get(f"{BASE_URL}/download/{file_id}", auth=USER_AUTH)
print(f"Status: {download_res.status_code} | Decrypted Content: {download_res.text.strip()}")

print("\n--- 3. Testing Unauthorized Access (RBAC Block) ---")
bad_res = requests.get(f"{BASE_URL}/download/{file_id}")
print(f"Status: {bad_res.status_code} | {bad_res.json()}")

print("\n--- 4. Generating 60-Second Temporary Link ---")
share_res = requests.get(f"{BASE_URL}/share/{file_id}", auth=USER_AUTH)
temp_url = share_res.json().get('link')
print(f"Temporary URL created: {temp_url}")

print("\n--- 5. Downloading via Temporary Link ---")
temp_dl_res = requests.get(temp_url)
print(f"Status: {temp_dl_res.status_code} | Decrypted Content: {temp_dl_res.text.strip()}")