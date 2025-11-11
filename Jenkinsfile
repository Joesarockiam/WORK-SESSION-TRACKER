pipeline {
  // Use 'agent any' to run on your main Jenkins node (which is Windows)
  agent any 
  environment {
    REGISTRY = "docker.io"
    DOCKER_REPO = "Joesarockiam/WORK-SESSION-TRACKER"
    BACKEND_IMAGE = "${env.DOCKER_REPO}:backend-${env.BUILD_NUMBER}"
    FRONTEND_IMAGE = "${env.DOCKER_REPO}:frontend-${env.BUILD_NUMBER}"
    DOCKER_CREDENTIALS_ID = "docker-hub-credentials"
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
          // Use 'bat' for Windows batch commands
          bat 'python -m pip install -r requirements.txt'
          bat 'pytest -q'
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
          docker.withRegistry("https://<${env.REGISTRY}>", env.DOCKER_CREDENTIALS_ID) {
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
          // Use 'bat' for Windows batch commands
          bat 'npm ci'
          bat 'npm run build'
        }
      }
    }

    stage('Build frontend image') {
      steps {
        script {
          docker.withRegistry("https://<${env.REGISTRY}>", env.DOCKER_CREDENTIALS_ID) {
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