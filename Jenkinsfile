pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/maryamtahirexe/assignmentpart2.git'
        TEST_REPO = 'https://github.com/maryamtahirexe/property-automation-tests.git'
        APP_IMAGE = 'property-app-image'
        TEST_IMAGE = 'property-test-image'
        APP_CONTAINER_NAME = 'property-app-container'
        APP_PORT = '3001'
    }

    stages {

        stage('Checkout Application Code') {
            steps {
                dir('app') {
                    git branch: 'main', url: "${APP_REPO}"
                }
            }
        }

        stage('Checkout Test Code') {
            steps {
                dir('tests') {
                    git branch: 'main', url: "${TEST_REPO}"
                }
            }
        }

        stage('Build Application Image') {
            steps {
                dir('app') {
                    script {
                        sh "docker build -t ${APP_IMAGE} ./my-app"
                    }
                }
            }
        }

        stage('Run Application Container') {
            steps {
                script {
                    sh """
                        echo "🛑 Stopping old container (if exists)..."
                        docker rm -f ${APP_CONTAINER_NAME} || true

                        echo "🚀 Starting new container..."
                        docker run -d --name ${APP_CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${APP_IMAGE}

                        echo "⏳ Waiting for app to be accessible on port ${APP_PORT}..."
                        for i in {1..20}; do
                            curl -s http://localhost:${APP_PORT} > /dev/null && break
                            echo "Waiting... ($i)"
                            sleep 2
                        done
                    """
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                dir('tests') {
                    script {
                        sh "docker build -t ${TEST_IMAGE} ."
                    }
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    sh """
                        echo "🧪 Running Selenium tests against http://localhost:${APP_PORT}..."
                        docker run --rm --network host ${TEST_IMAGE}
                    """
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            sh "docker rm -f ${APP_CONTAINER_NAME} || true"
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
