pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'sonar'
        DOCKERHUB = credentials('dockerhub')
        BACKEND_IMAGE = "joesarockiam/worktracker-backend"
        FRONTEND_IMAGE = "joesarockiam/worktracker-frontend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Joesarockiam/WORK-SESSION-TRACKER.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar') {
                    bat """
                    docker run --rm ^
                    -v "%cd%":/usr/src ^
                    sonarsource/sonar-scanner-cli ^
                    -Dsonar.projectKey=work-time-trackker ^
                    -Dsonar.sources=/usr/src ^
                    -Dsonar.host.url=http://host.docker.internal:9000 ^
                    -Dsonar.login=%SONARQUBE_AUTH_TOKEN%
                    """
                }
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                bat """
                docker build -t %BACKEND_IMAGE%:latest -f Dockerfile .
                """
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                bat """
                docker build -t %FRONTEND_IMAGE%:latest -f frontend/Dockerfile frontend
                """
            }
        }

        stage('Login to Docker Hub') {
            steps {
                bat """
                echo %DOCKERHUB_PSW% | docker login -u %DOCKERHUB_USR% --password-stdin
                """
            }
        }

        stage('Push Docker Images') {
            steps {
                bat """
                docker push %BACKEND_IMAGE%:latest
                docker push %FRONTEND_IMAGE%:latest
                """
            }
        }
    }

    post {
        success {
            echo "🎉 SonarQube + Docker Build + Push Successful!"
        }
        failure {
            echo "❌ Pipeline Failed!"
        }
    }
}
