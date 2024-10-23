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

        stage('Docker Compose Build') {
            steps {
                bat "docker-compose build --no-cache"
                // Builds the images without cache
            }
        }

        stage('Docker Compose Run') {
            steps {
                bat "docker-compose up -d"
                // Starts the containers in detached mode
            }
        }

        stage('Run Tests') {
            steps {
                bat "docker exec pytest_runner_works1 /opt/venv/bin/python -m pytest --alluredir=/tests_project/test_results/"
                // Runs the tests inside the Docker container
            }
        }

        stage('Copy Allure Results') {
            steps {
                bat "docker cp pytest_runner_works1:/tests_project/test_results . || true"
                // Copies the Allure results from the test runner container to the host into the current directory
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat "docker-compose run --rm test_runner allure generate /tests_project/test_results -o /tests_project/allure-report --clean"
                // Generates the Allure report inside the Docker container
            }
        }

        stage('Stop Docker Compose') {
            steps {
                bat "docker-compose down"
                // Stops and removes the containers, networks, volumes, and images created by `up`
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'allure-report/**/*', allowEmptyArchive: true
                // Archives the generated Allure report for future reference
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure results: [[path: 'allure-report']]
                // Publishes the Allure report in the Jenkins job interface
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
