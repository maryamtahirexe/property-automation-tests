pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/maryamtahirexe/assignmentpart2.git'
        TEST_REPO = 'https://github.com/maryamtahirexe/property-automation-tests.git'
        APP_IMAGE = 'property-app'
        TEST_IMAGE = 'property-tests'
    }

    stages {
        stage('Checkout Application') {
            steps {
                dir('app') {
                    git branch: 'main', url: "${APP_REPO}"
                }
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    git branch: 'main', url: "${TEST_REPO}"
                }
            }
        }

        stage('Build Application Docker Image') {
            steps {
                dir('app') {
                    script {
                        sh 'docker build -t ${APP_IMAGE} .'
                    }
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                dir('tests') {
                    script {
                        sh 'chmod +x run_tests.sh && docker build -t ${TEST_IMAGE} .'
                    }
                }
            }
        }

        stage('Start Application Container') {
            steps {
                script {
                    sh '''
                        # Stop and remove existing container
                        if docker ps -q --filter "name=property-app-container"; then
                            docker stop property-app-container || true
                            docker rm property-app-container || true
                        fi

                        # Free port 3000 if used
                        USED_CONTAINER=$(docker ps --filter "publish=3001" -q)
                        if [ ! -z "$USED_CONTAINER" ]; then
                            docker stop $USED_CONTAINER || true
                            docker rm $USED_CONTAINER || true
                        fi

                        # Start application container
                        docker run -d --name property-app-container -p 3001:3001 ${APP_IMAGE}

                        echo "⏳ Waiting for app to start..."
                        sleep 10
                    '''
                }
            }
        }

        stage('Run Tests Against App') {
            steps {
                script {
                    sh '''
                        echo "🚀 Running tests..."
                        docker run --rm --network host ${TEST_IMAGE}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Property app and test pipeline completed successfully.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
