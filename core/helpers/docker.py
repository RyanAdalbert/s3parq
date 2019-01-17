import boto3
import docker
import os
import base64

# Setting up some constants / runtime variables
# Should probably have a separate module for this?
cwd = os.getcwd()
DOCKERFILE_LOCATION = cwd+'/dockerfiles/core.dockerfile'
DOCKER_REPO = 'ichain/core'
my_session = boto3.session.Session()
AWS_REGION = my_session.region_name

docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
ecr_client = boto3.client('ecr')

# builds a docker image of the current state of the project and
# tags it with the current git branch.
def build_image(tag: str) -> str:
    full_tag = f"{DOCKER_REPO}:{tag}"
    response = [line for line in docker_client.build(
        path=cwd, dockerfile=DOCKERFILE_LOCATION, rm=True, tag=full_tag
    )]
    return full_tag

def remove_image(tag: str):
    full_tag = f"{DOCKER_REPO}:{tag}"
    docker_client.remove_image(full_tag)

def register_image(full_tag: str, account_id: str):
    repo = f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/{full_tag}"
    ecr_login(account_id)
    docker_client.tag(full_tag, repo)
    response = docker_client.push(repo)
    print(response)

#takes a single registry id and logs docker into the ECR Registry
def ecr_login(registry_id: str):
    ecr_response = ecr_client.get_authorization_token(registryIds=[registry_id])
    auth_data = ecr_response['authorizationData'][0]
    decoded_token = base64.b64decode(auth_data['authorizationToken']).decode("utf-8")
    user = decoded_token.split(':')[0]
    password = decoded_token.split(':')[1]
    registry_url = auth_data['proxyEndpoint']

    docker_response = docker_client.login(
        username=user,
        password=password,
        registry=registry_url,
        reauth=True
    )
    print(docker_response)

# docker tag ichain/gluestick:latest 687531504312.dkr.ecr.us-east-1.amazonaws.com/ichain/gluestick:latest