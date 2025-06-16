pipeline {
    agent any

    environment {
        APP_NAME = 'property-app'
        APP_PORT = '3002'
        CONTAINER_NAME = 'property_container'
        TEST_IMAGE = 'property-test-image'
        DISPLAY = ':99'
    }

    stages {
        stage('Clone Repositories') {
            steps {
                dir('app') {
                    git branch: 'main', url: 'https://github.com/maryamtahirexe/assignmentpart2.git'
                }
                dir('tests') {
                    git branch: 'main', url: 'https://github.com/maryamtahirexe/property-automation-tests.git'
                }
            }
        }

        stage('Build and Run App Container') {
            steps {
                dir('app') {
                    sh '''
                        echo "🔨 Building app container..."
                        docker build -t $APP_NAME .

                        echo "🧼 Removing existing app container..."
                        docker rm -f $CONTAINER_NAME || true

                        echo "🚀 Starting app container..."
                        docker run -d --name $CONTAINER_NAME -p $APP_PORT:$APP_PORT $APP_NAME

                        echo "⏳ Waiting for app to start..."
                        for i in {1..15}; do
                            if curl -s http://localhost:$APP_PORT > /dev/null; then
                                echo "✅ App is up!"
                                break
                            fi
                            echo "Attempt $i: App not ready yet, retrying..."
                            sleep 5
                        done

                        echo "🔍 Verifying app is accessible..."
                        curl -s http://localhost:$APP_PORT || (echo '❌ App not responding!' && exit 1)
                    '''
                }
            }
        }

        stage('Build Test Image and Run Tests') {
            steps {
                dir('tests') {
                    sh '''
                        echo "🐳 Building test image..."
                        docker build -t $TEST_IMAGE .

                        echo "🧪 Running Selenium tests in Docker..."
                        docker run --rm --network host $TEST_IMAGE
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up exited containers...'
            sh 'docker ps -a --filter "status=exited" -q | xargs -r docker rm'
        }

        success {
            echo '✅ All stages passed. Pipeline completed successfully.'
        }

        failure {
            echo '❌ Pipeline failed. Dumping logs for debugging.'
            sh "docker logs $CONTAINER_NAME || true"
        }
    }
}

