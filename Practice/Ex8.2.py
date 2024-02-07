import requests # Import reqests library to work with HTTP-requests
import time # Import time library to use sleep() function


# Function to create task and receive token and timeout
def create_task():
    url = "https://playground.learnqa.ru/ajax/api/longtime_job"
    response = requests.get(url) # Sending GET-request to the server to create a task
    result = response.json() # Parce the response in JSON format
    return result["token"], result["seconds"] # Return the token and timeout


# Function to verify the status of the token task
def check_task_status(task_token):
    url = f"https://playground.learnqa.ru/ajax/api/longtime_job"
    params = {"token": task_token}
    response = requests.get(url, params=params) # Sending GET-request to the server to verify the status of the task
    result = response.json()  # Parce the response in JSON format

    # Check the presence of "error" field
    if "error" in result:
        error_message = result['error']
        print(f"Error: {error_message}")
        if error_message != "No job linked to this token":
            print("Unexpected error message")

        if error_message == "No job linked to this token":
            print("The error message is as expected")
        return error_message

    return result["status"] # Return the status of the task


# Function to wait for a task running for a specified number of seconds
def wait_for_task_completion(seconds):
    print(f"Waiting for {seconds} seconds...") # Display a timeout message
    time.sleep(seconds) # Use sleep() function to delay program execution


# Function to get the result of the token task
def get_task_result(task_token):
    url = f"https://playground.learnqa.ru/ajax/api/longtime_job"
    params = {"token": task_token}
    response = requests.get(url, params=params) # Sending GET-request to the server to receive the result of the task
    result = response.json() # Parce the response in JSON format

    # Check the presence of "error" field
    if "error" in result:
        error_message = result['error']
        print(f"Error: {error_message}")
        if error_message != "No job linked to this token":
            print("Unexpected error message")
        if error_message == "No job linked to this token":
            print("The error message is as expected")

        return error_message

    return result # Return the result of the task


#Step 1: create a task and receive token and timeout
token, wait_seconds = create_task()
print(f"Task created with token: {token}")

# Step 2: check the status of the task before its completion
status_before_waiting = check_task_status(token)
print(f"Status before waiting: {status_before_waiting}")

# Step 3: wait for the number of seconds
wait_for_task_completion(wait_seconds)

# Step 4: check the status of the task  after waiting
status_after_waiting = check_task_status(token)
print(f"Status after waiting: {status_after_waiting}")

# Step 5: receive the result of the task (if it's ready)
if status_after_waiting == "Job is ready":
    task_result = get_task_result(token)
    if "error" not in task_result:
        print(f"Task result: {task_result['result']}")
else:
    print("Job is not ready")

# Step 6: check the request with invalid token
print("\n")
print("Checking sending of invalid token in request:")
invalid_token = "QNyoDOQNzMQNiNQNiMQNyQNAQN"
invalid_token_result = check_task_status(invalid_token)




