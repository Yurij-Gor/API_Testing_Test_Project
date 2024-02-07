import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
history = response.history

for redirect_response in history:
    print("URL:", redirect_response.url)
    print("Status Code:", redirect_response.status_code)
    print("Headers:", redirect_response.headers)
    print("\n")