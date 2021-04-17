pipeline {
    agent any
    triggers {
        pollSCM('*/5 * * * 1-5')
    }
    stages {

        stage('Build environment') {
            steps {
                sh '''curl -O https://bootstrap.pypa.io/get-pip.py
                      python3 get-pip.py --user
                      PATH="/var/lib/jenkins/.local/bin:$PATH"
                      pip install psutil
                      pip install pandas
                      pip install sqlalchemy
                      pip install winreg
                      pip install py-cpuinfo
                      export PYTHONPATH="${PYTHONPATH}:/computerMetricCollector"
                      python3 computerMetricCollector/InitiateCollectors.py
                    '''
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
