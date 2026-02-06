pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi"
        CONTAINER_NAME = "fastapi_container"
    }

    stages {
        stage('Clone Repo') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                docker run -d \
                    --name $CONTAINER_NAME \
                    -p 8000:8000 \
                    $IMAGE_NAME
                '''
            }
        }
    }
}
