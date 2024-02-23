pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Сборка Docker образа
                    docker.build("my-test-image:${env.BUILD_ID}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Запуск Docker контейнера для выполнения тестов
                    docker.run("my-test-image:${env.BUILD_ID}").inside {
                        sh 'pytest -v --alluredir=allure-results'
                        // Скопируйте результаты тестов из контейнера для генерации отчета
                        sh 'docker cp ${containerId}:/app/allure-results .'
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Генерация отчета Allure
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
