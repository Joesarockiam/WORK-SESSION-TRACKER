pipeline {
  agent any // Runs on your Windows agent
  environment {
    REGISTRY = "docker.io"
    
    // Lowercase for Docker Hub
    DOCKER_REPO = "joesarockiam/work-session-tracker" 
    
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
          // Use 'bat' for Windows
          bat 'python -m pip install -r requirements.txt'
          
          // Create the XML test report
          bat 'pytest --junitxml=test-results.xml'
        }
      }
      post {
        always {
          // This will now find the 'test-results.xml' file
          junit allowEmptyResults: true, testResults: '**/test-*.xml'
        }
      }
    }

    stage('Build backend image') {
      steps {
        script {
          // **THE FIX:** Removed angle brackets < > from the URL
          docker.withRegistry("https://${env.REGISTRY}", env.DOCKER_CREDENTIALS_ID) {
            def backendImage = docker.build("${env.BACKEND_IMAGE}", ".")
            backendImage.push()
            backendImage.tag("latest-backend")
            backendImage.push("latest-backend")
          }
        }
      }
    }

    stage('Frontend: build') {
      steps {
        dir('frontend') {
          // Use 'bat' for Windows
          bat 'npm ci'
          bat 'npm run build'
        }
      }
    }

    stage('Build frontend image') {
      steps {
        script {
          // **THE FIX:** Removed angle brackets < > from the URL
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
    }
  }
}
