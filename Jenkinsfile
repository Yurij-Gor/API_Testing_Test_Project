pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker Image
                    docker.build("my-test-image:${env.BUILD_ID}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Start Docker Container to Run Tests
                    docker.run("my-test-image:${env.BUILD_ID}").inside {
                        sh 'pytest -v --alluredir=allure-results'
                        // Copying test results from the report generation container
                        sh 'docker cp ${containerId}:/app/allure-results .'
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Allure report generation
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }
}
