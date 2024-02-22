# API Testing Test Project

## Description
This project is designed for the automation of API testing. It includes a series of tests written in Python that can be run against different environments.

## Technologies
This project is implemented using a variety of technologies and libraries to ensure high-quality API testing:

- Python 3.x: The core programming language used for writing test scripts.
- Requests Library: A simple, yet powerful HTTP library used for making API calls in Python. This library is chosen for its ease of use and its ability to handle various types of HTTP requests.
- Pytest: A robust framework for running the tests, providing features such as fixtures and markers that make writing and organizing tests easier.
- Allure: An open-source framework for test reporting, known for its ability to generate detailed and clear reports that include information about test execution and results.

Each of these technologies contributes to the project's ability to conduct thorough and effective API testing, ensuring the API's reliability and performance.

## Installation
To work with this project, you will need Python 3.x. Clone the repository and install the dependencies:

git clone https://github.com/Yurij-Gor/API_Testing_Test_Project

cd API_Testing_Test_Project

pip install -r requirements.txt


## Running Tests
To run the tests, set the environment variable `ENV` to `prod` (or other environments as needed) and execute the tests using pytest with allure reports:

$env:ENV="prod"; python -m pytest --alluredir=test_results/ tests/


## Project Structure
The project has the following structure:

```
API_Testing_Test_Project/
│
├── Practice/          # Additional practice files
├── lib/               # Libraries or additional modules
├── tests/             # Test directory
│   ├── conftest.py    # Test configuration file
│   ├── test_user_auth.py      # Test suite for user authentication
│   ├── test_user_delete.py    # Test suite for user deletion
│   ├── test_user_edit.py      # Test suite for user editing
│   ├── test_user_get.py       # Test suite for retrieving user data
│   └── test_user_register.py  # Test suite for user registration
├── .gitignore         # Specifies intentionally untracked files to ignore
├── Dockerfile         # Docker file for containerizing the application
├── docker-compose.yml # Docker compose file to define and run multi-container Docker applications
├── environment.py     # Environment configurations
└── requirements.txt   # Project dependencies
```
