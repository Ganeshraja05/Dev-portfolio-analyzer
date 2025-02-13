import requests

BASE_URL = "http://127.0.0.1:8000"



# Log in to get a JWT token
login_data = {
    "email": "test1@example.com",
    "password": "testpassword"
}
response = requests.post(f"{BASE_URL}/user/login", json=login_data)
login_response = response.json()
print("Login Response:", login_response)

# Extract the token
token = login_response.get("access_token")
if not token:
    raise Exception("Login failed; no token returned.")

headers = {"Authorization": f"Bearer {token}"}

# Retrieve the user profile
response = requests.get(f"{BASE_URL}/user/profile", headers=headers)
print("Profile Response:", response.json())

# Analyze a portfolio URL (replace with a valid URL)
portfolio_url = "https://my-portfolio-5ls.pages.dev/"
analyze_data = {"url": portfolio_url}
response = requests.post(f"{BASE_URL}/portfolio/analyze", headers=headers, json=analyze_data)
print("Portfolio Analysis Response:", response.json())
