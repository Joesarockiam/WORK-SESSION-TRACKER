pipeline {
  agent { label 'docker' } // or 'any' if your Jenkins agent has docker
  environment {
    REGISTRY = "docker.io"                      // DockerHub: docker.io, GitHub: ghcr.io
    DOCKER_REPO = "Joesarockiam/WORK-SESSION-TRACKER"   // Change 'joesarockiam' to your DockerHub username or ghcr.io/your-username
    BACKEND_IMAGE = "${env.DOCKER_REPO}:backend-${env.BUILD_NUMBER}"
    FRONTEND_IMAGE = "${env.DOCKER_REPO}:frontend-${env.BUILD_NUMBER}"
    DOCKER_CREDENTIALS_ID = "docker-hub-credentials"   // Match the Jenkins credential ID you created
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Backend: unit tests') {
      steps {
        dir('.') {
          // run pytest (adjust if your test command differs)
          sh 'python -m pip install -r requirements.txt'
          sh 'pytest -q'
        }
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: '**/test-*.xml' // optional, if you generate junit xml
        }
      }
    }

    stage('Build backend image') {
      steps {
        script {
          // login and push using withCredentials
          docker.withRegistry("https://${env.REGISTRY}", env.DOCKER_CREDENTIALS_ID) {
            def backendImage = docker.build("${env.BACKEND_IMAGE}", ".")
            backendImage.push()
            // also tag 'latest-backend' optionally
            backendImage.tag("latest-backend")
            backendImage.push("latest-backend")
          }
        }
      }
    }

    stage('Frontend: build') {
      steps {
        dir('frontend') {
          sh 'npm ci'
          sh 'npm run build'
        }
      }
    }

    stage('Build frontend image') {
      steps {
        script {
          docker.withRegistry("https://${env.REGISTRY}", env.DOCKER_CREDENTIALS_ID) {
            def frontendImage = docker.build("${env.FRONTEND_IMAGE}", "frontend")
            frontendImage.push()
            frontendImage.tag("latest-frontend")
            frontendImage.push("latest-frontend")
          }
        }
      }
    }

    stage('Optional: Deploy') {
      when { branch 'main' }
      steps {
        echo 'Add your deploy steps here (ssh, kubectl, docker-compose up, etc.)'
      }
    }
  }

  post {
    success {
      echo "Build #${env.BUILD_NUMBER} succeeded."
    }
    failure {
      echo "Build failed."
      // You can add email/Slack notifications here
    }
  }
}