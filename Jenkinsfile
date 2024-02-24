pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                bat "docker-compose down || true"
                bat "docker rm -f pytest_runner_works1 || true"
            }
        }

        stage('Docker Compose Build and Run') {
            steps {
                bat "docker-compose up --build -d"
            }
        }

        stage('Copy Allure Results') {
            steps {
                bat "docker cp pytest_runner_works1:/tests_project/test_results allure_results || true"
            }
        }

        stage('Stop Docker Compose') {
            steps {
                bat "docker-compose down"
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat "allure generate allure_results -o allure_report --clean"
                // bat "allure serve allure_results" // Use this line if you want to serve the report instead of generating static files
            }
        }
    }
}
