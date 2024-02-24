pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                bat "docker-compose down || true"
                bat "docker rm -f pytest_runner_works1 || true"
                // Ensures a clean state before starting the test run
            }
        }

        stage('Docker Compose Build and Run') {
            steps {
                bat "docker-compose up --build -d"
                // Builds and starts the test runner and Allure Docker Service in detached mode
            }
        }

        stage('Copy Allure Results') {
            steps {
                bat "docker cp pytest_runner_works1:/tests_project/test_results allure_results || true"
                // Copies the Allure results from the test runner container to the host
            }
        }

        stage('Stop Docker Compose') {
            steps {
                bat "docker-compose down"
                // Stops and removes the containers, networks, volumes, and images created by `up`
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat "allure generate allure_results -o allure_report --clean"
                // Generates the Allure report from the results
                // This step is optional if you're using Allure Docker Service to serve the reports dynamically
            }
        }
    }
}
