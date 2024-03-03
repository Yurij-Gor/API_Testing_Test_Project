pipeline {
    agent any

    tools {
        // Defines Allure as a tool to be used
        allure 'allure_commandline'
    }

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
                bat "docker cp pytest_runner_works1:/tests_project/test_results . || true"
                // Copies the Allure results from the test runner container to the host into the current directory
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
                bat "docker-compose run --rm test_runner allure generate /tests_project/test_results -o /tests_project/allure-report --clean"
            }
        }

        stage('Archive Results') {
            steps {
                // Archives Allure results and reports for future reference
                archiveArtifacts artifacts: 'allure-report/**/*', allowEmptyArchive: true
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure results: [[path: 'allure-report']]
            }
        }
    }

    post {
        always {
            mail to: 'yurij.chernogorcev2@gmail.com',
                 subject: "Test Report for ${env.JOB_NAME}",
                 body: "The test report is available at: ${env.BUILD_URL}artifact/allure-report/index.html"
            // Sends an email notification about the build status with a link to the Allure report
        }
    }
}