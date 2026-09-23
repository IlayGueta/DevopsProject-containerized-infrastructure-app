pipeline {
    agent any

    environment {
        APP_NAME = 'ilay-infrastructure-api'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building ${env.APP_NAME}"
                echo "Build Number: ${env.BUILD_NUMBER}"

                sh "docker build -t ${env.APP_NAME}:${env.BUILD_NUMBER} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ilay-dockerhub',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    )
                ]) {
                    echo "Deploying with username ${env.USERNAME}"

                    sh 'echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin'
                    sh "docker tag ${env.APP_NAME}:${env.BUILD_NUMBER} ${env.USERNAME}/${env.APP_NAME}:${env.BUILD_NUMBER}"
                    sh "docker push ${env.USERNAME}/${env.APP_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Run Docker Image') {
            steps {
                echo "Running ${env.APP_NAME}:${env.BUILD_NUMBER}"

                sh "docker run -d --name infrastructure-api-test -p 5001:5000 ${env.APP_NAME}:${env.BUILD_NUMBER}"
            }
        }

        stage('Health') {
            steps {
                sh "sleep 10"
                sh "curl --fail http://host.docker.internal:5001/health"
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                // Test steps here
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Deploy steps here
            }
        }
    }

    post {
        always {
            sh 'docker rm -f infrastructure-api-test || true'
        }
        failure {
            echo 'The pipeline failed!'
        }
        success {
            echo 'The pipeline finished successfully!'
        }
    }
}