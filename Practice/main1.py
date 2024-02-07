import requests

# Set up payload with login and password
payload ={"login": "secret_login", "password": "secret_password"}

# Step 1: Make a POST request to get the authentication cookie
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

# Retrieve the 'auth_cookie' value from the response cookies
cookie_value = response1.cookies.get('auth_cookie')

# Create a dictionary to store cookies if 'auth_cookie' is present
cookies ={}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})

# Step 2: Make a POST request to check authentication using the obtained cookie
response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

# Print the response text from the second request
print(response2.text)


