pipeline {
    agent any

    environment {
        TEST_IMAGE = 'property-test-image'
    }

    stages {
        stage('Clone Tests Repo') {
            steps {
                dir('tests') {
                    git branch: 'main', url: 'https://github.com/maryamtahirexe/property-automation-tests.git'
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
        }
    }
}

