pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t my-test-image:${env.BUILD_ID} .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh "docker run --name test-container-${env.BUILD_ID} my-test-image:${env.BUILD_ID} pytest -v --alluredir=allure-results"
                    sh "docker cp test-container-${env.BUILD_ID}:/app/allure-results ."
                    sh "docker stop test-container-${env.BUILD_ID}"
                    sh "docker rm test-container-${env.BUILD_ID}"
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    sh 'allure generate allure-results --clean -o allure-report'
                }
            }
        }
    }
}