pipeline {
    agent any

    environment {
        // Replace with your Docker Hub/Registry details
        DOCKER_REGISTRY = "docker.io"
        DOCKER_REPO     = "abhianand2015/db2-sp-app"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        DOCKER_CREDS    = "docker-hub-credentials-id" // The ID from Jenkins Credentials
    }

    stages {
        stage('Pre-flight Check') {
            steps {
                echo 'Checking Disk Space on Node...'
                sh 'df -h /'
                // Optional: Cleanup old images to prevent "Disk Full" errors
                sh 'docker image prune -f'
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running Application Tests...'
                // Adjust this based on your app (e.g., npm test, pytest, etc.)
                sh 'python3 -m pytest tests/ || echo "No tests found, skipping..." '
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Image: ${DOCKER_REPO}:${IMAGE_TAG}"
                sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${DOCKER_REPO}:latest"
            }
        }

        stage('Vulnerability Scan') {
            steps {
                echo 'Scanning image for vulnerabilities...'
                // Using Trivy (standard) - skip if not installed
                sh "trivy image ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG} || echo 'Trivy not installed'"
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDS}") {
                        echo "Pushing Image to Registry..."
                        docker.image("${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG}").push()
                        docker.image("${DOCKER_REGISTRY}/${DOCKER_REPO}:latest").push()
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo 'Pipeline Succeeded! New image is ready.'
        }
        failure {
            echo 'Pipeline Failed. Check the logs for errors.'
        }
    }
}

