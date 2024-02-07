# Import the json module to work with JSON data
import json

# JSON-formatted text representing a list of messages
json_text = ('{"messages": [{"message":"This is the first message","timestamp":"2021-06-04 16:40:53},{"message":"And '
             'this is the second message","timestamp":"2021-06-04 16:41:01"}]}')

# Load the JSON text into a Python object
obj = json.loads(json_text)

# Extract information from the loaded JSON object
first_message = obj['messages'][0]['message']
first_message_timestamp = obj['messages'][0]['timestamp']

second_message = obj['messages'][1]['message']
second_message_timestamp = obj['messages'][1]['timestamp']

# Display the information
print(first_message)
print(f"Time: {first_message_timestamp}")

print(second_message)
print(f"Time: {second_message_timestamp}")


