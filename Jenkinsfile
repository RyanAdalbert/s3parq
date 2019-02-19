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
        sh "script/ci_test"
    }
    stage ('Deploy') {
        echo "We are currently working on branch: ${env.BRANCH_NAME}"

        switch (env.BRANCH_NAME) {
            // No "overall" dev branch for now, this will be done on the developer's
            // machine and the artifacts will have the git branch name in them.
            // case 'master': 
            //     env.DEPLOYMENT_ENVIRONMENT = 'dev';
            //     break;
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
            sh "script/ci_shell 'ICHAIN_ENVIRONMENT=${env.DEPLOYMENT_ENVIRONMENT} corecli publish'"
        }
    }
    stage ('Cleanup') {
        // Jenkins will need to be able to talk to the sandbox account in order to run the 
        // tidy local command.
        // sh "script/ci_shell 'corecli tidy local'"
    }
}