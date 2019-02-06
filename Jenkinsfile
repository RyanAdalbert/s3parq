node {
    stage ('Checkout') {
        // Clean workspace before checkout
        step ([$class: 'WsCleanup'])
        checkout scm
    }
    stage('Build') {
        echo "Building..."
    }
    stage('Test') {
        echo "Testing..."
        echo "User is $USER"
        sh "script/ci_test"
    }
    stage ('Deploy') {
        echo "We are currently working on branch: ${env.BRANCH_NAME}"

        switch (env.BRANCH_NAME) {
            case 'master': 
                env.DEPLOYMENT_ENVIRONMENT = 'dev';
                break;
            case 'uat': 
                env.DEPLOYMENT_ENVIRONMENT = 'uat';
                break;
            case 'prod': 
                env.DEPLOYMENT_ENVIRONMENT = 'prod';
                break;
            default: env.DEPLOYMENT_ENVIRONMENT = 'no_deploy';
        }
        if (env.DEPLOYMENT_ENVIRONMENT != 'no_deploy') {
            echo "Trying to deploy to ${env.DEPLOYMENT_ENVIRONMENT}."
            sh "script/ci_shell 'corecli publish ${env.DEPLOYMENT_ENVIRONMENT}'"
        }
    }
    stage ('Cleanup') {
        sh "script/ci_shell 'corecli tidy local'"
    }
}