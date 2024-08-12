pipeline {
    agent {
        docker { image 'docker:dind' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'docker compose build'
                sh 'docker compose push'
            }
        }
    }
}
