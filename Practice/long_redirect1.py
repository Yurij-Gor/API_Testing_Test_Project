import requests

# Sending a GET request to a URL with long redirects
response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

# Getting the history of the request (a list of Response objects for each redirect)
all_redirections = response.history

# Printing the URLs of all redirections
print("Redirections:")
for element in all_redirections:
    print(element.url)

# Adding a newline for better readability
print("\n")

# Counting the total number of redirections
count_of_redirections = len(all_redirections)
print(f"Quantity of redirections: {count_of_redirections}")

# Adding more space for separation
print("\n")

# Printing the final URL after all the redirections
final_destination = response
print(f"Final URL: {final_destination.url}")


