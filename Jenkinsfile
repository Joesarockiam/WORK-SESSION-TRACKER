pipeline {
    agent any

    environment {
        // SonarQube server name (configured in Manage Jenkins → Configure System)
        SONARQUBE_SERVER = 'sonar'         

        // Docker Hub credentials ID stored in Jenkins
        DOCKERHUB = credentials('dockerhub')

        // Docker image names
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
                withSonarQubeEnv('sonar') {    // uses sonar-token internally
                    bat """
                    sonar-scanner ^
                    -Dsonar.projectKey=work-time-trackker ^
                    -Dsonar.sources=. ^
                    -Dsonar.host.url=%SONAR_HOST_URL% ^
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
            echo "🎉 Build + SonarQube + Docker Build + Docker Push — COMPLETED SUCCESSFULLY!"
        }
        failure {
            echo "❌ Build Failed!"
        }
    }
}
