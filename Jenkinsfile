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
                script {
                    // Ensure Allure CLI is available
                    def allureExecutable = tool 'allure_commandline'
                    bat "${allureExecutable}/bin/allure generate test_results -o allure_report --clean"
                    // Generates the Allure report from the results in 'test_results' directory
                }
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
                // Publishes Allure report into Jenkins build dashboard
                allure([
                    reportPaths: ['allure-report'],
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            mail to: 'email1@example.com,email2@example.com',
                 subject: "Build ${currentBuild.fullDisplayName}",
                 body: "The build was ${currentBuild.currentResult}: Check the report at ${env.BUILD_URL}allure/"
            // Sends an email notification about the build status with a link to the Allure report
        }
    }
}
