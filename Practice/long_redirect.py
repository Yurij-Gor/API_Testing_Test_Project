import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
all_redirections = response.history

print("Redirections:")
for element in all_redirections:
    print(element.url)

print("\n")

count_of_redirections = len(all_redirections)
print(f"Quantity of redirections: {count_of_redirections}")

print("\n")
final_destination = response
print(f"Final URL: {final_destination.url}")
