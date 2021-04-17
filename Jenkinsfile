pipeline {
    agent any
    triggers {
        pollSCM('*/5 * * * 1-5')
    }
    stages {

        stage('Build environment') {
            steps {
                git credentialsId: '980349b4-87ae-4cb4-be9e-a0fbf1779374', url: 'https://github.com/yilin6867/MSCS_710_Software_Project.git'
                sh 'python3 MSCS_710_Software_Project/computerMetricCollector/InitiateCollectors.py'
            }
        }
        stage('Test environment') {
            steps {
                echo "testing environment started"
            }
        }
    }
    post {
        always {
            sh 'conda remove --yes -n ${BUILD_TAG} --all'
        }
        failure {
            echo "Send e-mail, when failed"
        }
    }
}
