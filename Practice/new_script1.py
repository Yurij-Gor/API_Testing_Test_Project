import requests

# Sending a GET request to a URL with long redirects
response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
# Getting the history of the request (a list of Response objects for each redirect)
history = response.history

# Iterating through each redirect response in the history
for redirect_response in history: # Printing information about each redirect response
    print("URL:", redirect_response.url)
    print("Status Code:", redirect_response.status_code)
    print("Headers:", redirect_response.headers)
    print("\n")
    


