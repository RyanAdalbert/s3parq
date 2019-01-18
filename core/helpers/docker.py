import boto3
import docker
import os
import base64

# Setting up some constants / runtime variables
# Should probably have a separate module for this?
cwd = os.getcwd()
DOCKERFILE_LOCATION = cwd+'/dockerfiles/core.dockerfile'
my_session = boto3.session.Session()
AWS_REGION = my_session.region_name

docker_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
ecr_client = boto3.client('ecr')

# builds a docker image of the current state of the project and tags it
def build_image(full_tag: str) -> str:
    # Need to figure out a way to see see that this image didn't fail building
    response = [line for line in docker_api_client.build(
        path=cwd, dockerfile=DOCKERFILE_LOCATION, rm=True, tag=full_tag
    )]
    return full_tag

def remove_image(full_tag: str):
    image = docker_client.images.get(full_tag)
    response = docker_api_client.remove_image(full_tag)
    print(response)

def remove_ecr_image(tag: str, repo_name: str, account_id: str):
    ecr_login(account_id)
    full_tag = f"{repo_name}:{tag}"
    ecr_tagged_image_name = get_aws_repository(full_tag, account_id)
    image = docker_client.images.get(ecr_tagged_image_name)
    repo_digest = image.attrs['RepoDigests'][0]

    digest_sha = repo_digest.split("@")[-1]

    # remove the image from ECR
    response = ecr_client.batch_delete_image(
        registryId=account_id,
        repositoryName=repo_name,
        imageIds=[
            {
                'imageDigest': digest_sha,
                'imageTag': tag
            },
        ]
    )
    # remove the local image
    docker_api_client.remove_image(ecr_tagged_image_name)
    print(response)

def register_image(full_tag: str, account_id: str):
    repo = get_aws_repository(full_tag, account_id)
    ecr_login(account_id)
    docker_api_client.tag(full_tag, repo)
    response = docker_api_client.push(repo)
    print(response)

#takes a single registry id and logs docker into the ECR Registry
def ecr_login(registry_id: str):
    ecr_response = ecr_client.get_authorization_token(registryIds=[registry_id])
    auth_data = ecr_response['authorizationData'][0]
    decoded_token = base64.b64decode(auth_data['authorizationToken']).decode("utf-8")
    user = decoded_token.split(':')[0]
    password = decoded_token.split(':')[1]
    registry_url = auth_data['proxyEndpoint']

    docker_response = docker_api_client.login(
        username=user,
        password=password,
        registry=registry_url,
        reauth=True
    )
    # print(docker_response)

def get_aws_repository(full_tag: str, account_id: str) -> str:
    return f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/{full_tag}"