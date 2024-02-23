pipeline {
    agent any

    stages {
        stage('Docker Compose Build and Run') {
            steps {
                bat "docker-compose up --build -d"
            }
        }

        stage('Copy Allure Results') {
            steps {
                bat "docker cp pytest_runner_works1:/tests_project/test_results allure_results"
            }
        }

        stage('Stop Docker Compose') {
            steps {
                bat "docker-compose down"
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat "allure serve allure_results"
            }
        }
    }
}
