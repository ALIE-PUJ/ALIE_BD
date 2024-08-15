pipeline {
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: docker
            image: docker:dind
            ports:
              - name: dind-con-port
                containerPort: 2376
                hostPort: 2376
                protocol: TCP
            volumeMounts:
              - name: dind-storage
                mountPath: /var/lib/docker
            env:
              - name: DOCKER_HOST
                value: "tcp://localhost:2376"
              - name: DOCKER_TLS_CERTDIR
                value: '/certs'
              - name: DOCKER_CERT_PATH
                value: '/certs/client'
              - name: DOCKER_TLS_VERIFY
                value: "1"
            tty: true
            securityContext:
              privileged: true
          volumes:
          - name: dind-storage
            persistentVolumeClaim:
              claimName: dind-storage
        '''
    }
  }
  stages {
    stage('Build-Docker-Image') {
      steps {
        container('docker') {
          sh 'docker compose build'
        }
      }
    }
    stage('Push-Images-Docker-to-DockerHub') {
      steps {
        container('docker') {
          sh 'docker compose push'
        }
      }
    }
  }
}