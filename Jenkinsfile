pipeline {
  agent any

  environment {
    SCM_URL = 'git@github.com:lordoftheflies/muadib-notebook.git'
    SLACK_BASE_URL = 'https://cherubits.slack.com/services/hooks/jenkins-ci/'
    MASTER_BRANCH = 'master'
    DEVELOP_BRANCH = 'develop'
    CREDENTIALS = 'credentials-github-lordoftheflies-ssh'
    SUDO_PASSWORD = 'Armageddon0'

    VIRTUAL_ENVIRONMENT_DIRECTORY = 'env'
    PYTHON_EXECUTABLE = '/usr/bin/python3.4'
  }

  stages {
    stage('Prequisites') {
      steps {
        git(url: "${SCM_URL}", branch: "${DEVELOP_BRANCH}", changelog: true, credentialsId: "${CREDENTIALS}", poll: true)

        sh '''if [ ! -d "$VIRTUAL_ENVIRONMENT_DIRECTORY" ]; then
            virtualenv --no-site-packages -p $PYTHON_EXECUTABLE $VIRTUAL_ENVIRONMENT_DIRECTORY
        fi
        '''
      }
    }

    stage('Build') {
      steps {
        echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
        echo 'Building..'

        slackSend color: 'good', message: "$JOB_NAME started new build ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"

        sh '''. ./env/bin/activate
            pip install -r requirements.txt
            deactivate
        '''

        sh '''. ./env/bin/activate
            python manage.py collectstatic --noinput
            deactivate
        '''
        sh '''. ./env/bin/activate
            python manage.py migrate
            deactivate
        '''
        sh '''. ./env/bin/activate
            python setup.py sdist develop
            deactivate
        '''

        slackSend color: 'good', message: "$JOB_NAME finished build ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"

      }
    }
    stage('Test') {
      steps {
        echo 'Testing..'
        sh '''. ./env/bin/activate
            python -m unittest discover tests/ -p '*_test.py'
            deactivate
        '''
        slackSend color: 'good', message: "$JOB_NAME tested. ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"
      }
    }
    stage('Deploy staging') {
      steps {
        echo 'Deploying locally ...'
        sh '''. ./env/bin/activate
            python setup.py sdist install
            deactivate
        '''
        slackSend color: 'good', message: "$JOB_NAME deployed build ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"
      }
    }
    stage('Distribute') {
      steps {
        echo 'Ditribute....'
        sh '''. ./env/bin/activate
            python scrapersite/setup.py sdist upload -r local
            deactivate
        '''
        slackSend color: 'good', message: "$JOB_NAME distributed build ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"

      }
    }
    stage('Deploy site') {
      steps {
        echo 'Deploying site ...'
        sh '''cd ./ansible
            ansible-playbook ./site.yml --extra-vars "ansible_become_pass=Armageddon0"
        '''
        slackSend color: 'good', message: "$JOB_NAME deployed demo build ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"

      }
    }
  }

  post {
    always {
      slackSend color: 'warning', message: "$JOB_NAME build summary ${env.BUILD_NUMBER} (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"
    }
    failure {
      slackSend color: 'good', message: "$JOB_NAME build ${env.BUILD_NUMBER} failed. (<$BUILD_URL|Open>)", baseUrl: "$SLACK_BASE_URL", botUser: true, channel: 'jenkins', teamDomain: 'cherubits', tokenCredentialId: "${CREDENTIALS}"
    }
  }
}

