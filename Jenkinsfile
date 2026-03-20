pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "docker.io"
        DOCKER_CREDS    = "docker-hub-credentials-id"
        // Repos for both images
        FRONT_REPO      = "abhianand2015/db2-sp-frontend-git"
        BACK_REPO       = "abhianand2015/db2-sp-backend-git"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
    }

    stages {
        stage('Pre-flight & Cleanup') {
            steps {
                sh 'df -h /'
                sh '/opt/homebrew/bin/docker image prune -f'
            }
        }
  
        stage('Build and Push Images') {
            parallel {
                stage('Frontend') {
                        steps {
                            dir('frontend') { // Switch to frontend directory
                                echo "Building Frontend..."
                                sh """/opt/homebrew/bin/docker  build --platform linux/amd64  --build-arg VITE_API_BASE="http://192.168.1.12:30008/api/v1"   -t ${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG} ."""
                                sh "/opt/homebrew/bin/docker tag ${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${FRONT_REPO}:latest"
                                
                                withCredentials([usernamePassword(
                                    credentialsId: DOCKER_CREDS,
                                    usernameVariable: 'DOCKER_USER',
                                    passwordVariable: 'DOCKER_PASS'
                                )]) {
                                    sh """
                                    echo \$DOCKER_PASS | /opt/homebrew/bin/docker login -u \$DOCKER_USER --password-stdin ${DOCKER_REGISTRY}
                                    /opt/homebrew/bin/docker push ${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG}
                                    /opt/homebrew/bin/docker push ${DOCKER_REGISTRY}/${FRONT_REPO}:latest
                                    """
                                }
                            }
                        }
                    }

                stage('Backend') {
                    steps {
                        dir('backend') { // Switch to backend directory
                            echo "Building Backend..."
                            sh "/opt/homebrew/bin/docker  build --platform linux/amd64 -t ${DOCKER_REGISTRY}/${BACK_REPO}:${IMAGE_TAG} ."
                            sh "/opt/homebrew/bin/docker tag ${DOCKER_REGISTRY}/${BACK_REPO}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${BACK_REPO}:latest"
                            
                                withCredentials([usernamePassword(
                                    credentialsId: DOCKER_CREDS,
                                    usernameVariable: 'DOCKER_USER',
                                    passwordVariable: 'DOCKER_PASS'
                                )]) {
                                    sh """
                                    echo \$DOCKER_PASS | /opt/homebrew/bin/docker login -u \$DOCKER_USER --password-stdin ${DOCKER_REGISTRY}
                                    /opt/homebrew/bin/docker push ${DOCKER_REGISTRY}/${FRONT_REPO}:${IMAGE_TAG}
                                    /opt/homebrew/bin/docker push ${DOCKER_REGISTRY}/${FRONT_REPO}:latest
                                    """
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
