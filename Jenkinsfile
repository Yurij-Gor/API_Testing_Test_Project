pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                bat "docker build -t my-test-image:${env.BUILD_ID} ."
            }
        }

        stage('Run Tests') {
            steps {
                bat "docker run --name test-container-${env.BUILD_ID} my-test-image:${env.BUILD_ID} pytest -v --alluredir=allure-results"
                bat "docker cp test-container-${env.BUILD_ID}:/app/allure-results ."
                bat "docker stop test-container-${env.BUILD_ID}"
                bat "docker rm test-container-${env.BUILD_ID}"
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat 'allure generate allure-results --clean -o allure-report'
            }
        }
    }
}
