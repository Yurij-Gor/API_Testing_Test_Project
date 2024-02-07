import json

# A string in JSON format
string_as_json_format = '{"answer": "Hello, User"}'

# Parsing the JSON string into a Python object
obj = json.loads(string_as_json_format)

# Key to check in the JSON object
key = "answer"

# Checking if the key is present in the JSON object
if key in obj:
    # If the key is present, print its corresponding value
    print(obj[key])
else:
    # If the key is not present, print a message indicating its absence
    print(f"There is no key {key} in JSON format")





