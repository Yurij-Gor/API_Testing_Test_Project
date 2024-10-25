pipeline {
    agent any

    environment {
    LANG = 'C.UTF-8'
    LC_ALL = 'C.UTF-8'
    }

    tools {
        // Defines Allure as a tool to be used
        allure 'allure_commandline'
    }

    stages {
        stage('Cleanup') {
            steps {
                bat "docker-compose down --volumes --remove-orphans || true"
                // Cleans up containers, volumes, and orphan containers but doesn't remove the image
                bat "docker rm -f pytest_runner_works1 || true"
                // Ensures any previous containers are removed
            }
        }

        stage('Docker Compose Build and Run') {
            steps {
                bat "docker-compose build"
                // Only rebuilds the image if there are changes
                bat "docker-compose up -d"
                // Starts the services in detached mode
            }
        }

        stage('Run Tests') {
            steps {
                bat "docker exec pytest_runner_works1 /opt/venv/bin/python -m pytest --alluredir=/tests_project/test_results/ || true"
                // Runs the tests but doesn't fail the pipeline if tests fail (allows completion)
            }
            post {
                always {
                    echo 'Tests completed, proceeding with report generation...'
                }
            }
        }

        stage('Copy Allure Results') {
            steps {
                bat "docker cp pytest_runner_works1:/tests_project/test_results . || true"
                // Copies the Allure results from the test runner container to the host into the current directory
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test_results/**/*', allowEmptyArchive: true
                    // Ensures the results are archived even if the tests fail
                }
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
                bat "docker-compose down --volumes --remove-orphans"
                // Stops the services and cleans up the associated volumes and orphaned containers
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'allure-report/**/*', allowEmptyArchive: false
                // Archives the generated Allure report if it exists (ensures that empty archives are not allowed)
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
