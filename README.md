# API Testing Test Project

## Description
This project is designed for the automation of API testing and showcases a custom-built testing framework housed within the `lib/` directory. Project includes a series of tests written in Python that can be run against different environments. It also uses local Jenkins for CI/CD, Docker for containerization, and Docker Compose for multi-container orchestration, to simulate the full testing workflow.

## Test Results
View the Allure Test Report:  
[Allure Report](https://yurij-gor.github.io/API_Testing_Test_Project/)

## Technologies
This project is implemented using a variety of technologies and libraries to ensure high-quality API testing:

- Python 3.x: The core programming language used for writing test scripts.
- Requests Library: A simple, yet powerful HTTP library used for making API calls in Python. This library is chosen for its ease of use and its ability to handle various types of HTTP requests.
- Pytest: A robust framework for running the tests, providing features such as fixtures and markers that make writing and organizing tests easier.
- Allure: An open-source framework for test reporting, known for its ability to generate detailed and clear reports that include information about test execution and results.
- Docker: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.
- Docker Compose: A tool for defining and running multi-container Docker applications.
- Jenkins: An open-source automation server that enables developers around the world to reliably build, test, and deploy their software.

Each of these technologies contributes to the project's ability to conduct thorough and effective API testing, ensuring the API's reliability and performance.

## Installation
To work with this project, you will need Python 3.x. Clone the repository and install the dependencies:
```
git clone https://github.com/Yurij-Gor/API_Testing_Test_Project

cd API_Testing_Test_Project

pip install -r requirements.txt
```

## Running Tests
To run the tests, set the environment variable `ENV` to `prod` (or to `dev`) and execute the tests using pytest with allure reports:

```powershell
$env:ENV="prod"; python -m pytest --alluredir=test_results/ tests/
```

After running the test, start generating a report: 

```
allure serve test_results
```

## Running Tests in Docker
To run the tests inside a Docker container, make sure you have Docker installed on your system. Then, execute the following commands:

```bash
docker-compose down
docker pull python
docker build -t pytest_runner .
docker-compose up --build
```

This will ensure that the Docker environment is clean before starting, pull the latest Python image, build the test runner image, and then start the services as defined in your docker-compose.yml file.

## Viewing Allure Report with Docker
After running your tests in Docker, you can copy the test results from the Docker container to your local machine and view the Allure report using the following commands:

Replace `<YourLocalPath>` with the path where you want to store the test results on your local machine.

```bash
docker cp pytest_runner_works1:/tests_project/test_results <YourLocalPath>/allure_results
```
To view the Allure report, run:
```
allure serve <YourLocalPath>/allure_results/test_results
```
This command will start a web server to serve your Allure report, which you can view in your web browser.

## Project Structure
The project has the following structure:

```
API_Testing_Test_Project/
│
├── Practice/          # Additional practice files
├── lib/               # Libraries or additional modules
│ ├── init.py                # Package initializer for the testing framework
│ ├── assertions.py          # Assertions helpers
│ ├── base_case.py           # Base test case setup with common test initialization methods
│ ├── logger.py              # Custom logger for streamlined test output and logging
│ └── my_requests.py         # HTTP request helpers for simplified API interaction
├── tests/             # Test directory
│ ├── init.py                # Test package initializer
│ ├── conftest.py            # Test configuration file
│ ├── test_user_auth.py      # Test suite for user authentication
│ ├── test_user_delete.py    # Test suite for user deletion
│ ├── test_user_edit.py      # Test suite for user editing
│ ├── test_user_get.py       # Test suite for retrieving user data
│ └── test_user_register.py  # Test suite for user registration
├── .gitignore         # Specifies intentionally untracked files to ignore
├── Dockerfile         # Docker file for containerizing the application
├── docker-compose.yml # Docker compose file to define and run multi-container Docker applications
├── environment.py     # Environment configurations
├── Jenkinsfile        # Defines the Jenkins pipeline for continuous integration
├── README.md          # The project's README file providing detailed informatio
└── requirements.txt   # Project dependencies
```
