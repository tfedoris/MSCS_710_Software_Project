pipeline{
    agent {
    label 'main'
    }
    stages{
        stage("git"){
            steps{
                git branch: 'main', credentialsId: 'tim github', url: 'https://github.com/tfedoris/MSCS_710_Software_Project.git'
            }
        }
        stage("test run"){
            steps{
                powershell '''ls
                    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString("https://chocolatey.org/install.ps1"))
                    '''
                bat '''C:\\ProgramData\\chocolatey\\bin\\choco feature enable -n allowGlobalConfirmation
                    C:\\ProgramData\\chocolatey\\bin\\choco.exe install python --version=3.8.0
                    C:\\python38\\scripts\\pip.exe install --upgrade pip
                    C:\\python38\\scripts\\pip.exe install psutil
                    C:\\python38\\scripts\\pip.exe install pandas
                    C:\\python38\\scripts\\pip.exe install sqlalchemy
                    C:\\python38\\scripts\\pip.exe install py-cpuinfo
                    C:\\python38\\scripts\\pip.exe install pycryptodomex
                    C:\\python38\\scripts\\pip.exe install requests
                    C:\\python38\\python.exe -m computerMetricCollector.__init__ -t True
                    '''
            }
        }
        stage('Test environment') {
            steps {
                echo "testing environment started"
            }
        }
    }
}
