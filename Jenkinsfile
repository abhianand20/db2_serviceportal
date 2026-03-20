pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "docker.io"
        DOCKER_CREDS    = "docker-hub-credentials-id"
        // Repos for both images
        FRONT_REPO      = "abhianand2015/db2-sp-frontend-git"
        BACK_REPO       = "abhianand2015/db2-sp-backend-git"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Pre-flight & Cleanup') {
            steps {
                sh 'df -h /'
                sh '/opt/homebrew/bin/docker image prune -f'
            }
        }
 docker build --build-arg VITE_API_BASE="http://192.168.1.12:30008/api/v1" -t abhianand2015/db2-sp-frontend-1:latest . 
        stage('Build and Push Images') {
            parallel {
                stage('Frontend') {
                    steps {
                        dir('frontend') { // Switch to frontend directory
                            echo "Building Frontend..."
                            sh """/opt/homebrew/bin/docker build  --build-arg VITE_API_BASE="http://192.168.1.12:30008/api/v1"   -t ${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG} ."""
                            sh "/opt/homebrew/bin/docker tag ${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${FRONT_REPO}:latest"
                            
                            script {
                                docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDS}") {
                                    docker.image("${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG}").push()
                                    docker.image("${DOCKER_REGISTRY}/${FRONT_REPO}:latest").push()
                                }
                            }
                        }
                    }
                }

                stage('Backend') {
                    steps {
                        dir('backend') { // Switch to backend directory
                            echo "Building Backend..."
                            sh "/opt/homebrew/bin/docker buildx build --platform linux/amd64,linux/arm64  -t ${DOCKER_REGISTRY}/${BACK_REPO}:${IMAGE_TAG} ."
                            sh "/opt/homebrew/bin/docker tag ${DOCKER_REGISTRY}/${BACK_REPO}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${BACK_REPO}:latest"
                            
                            script {
                                docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDS}") {
                                    docker.image("${DOCKER_REGISTRY}/${BACK_REPO}:${IMAGE_TAG}").push()
                                    docker.image("${DOCKER_REGISTRY}/${BACK_REPO}:latest").push()
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
