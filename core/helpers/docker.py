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
batch_client = boto3.client('batch')

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
    return response

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
    return response

def register_image(tag: str, repo_name: str, account_id: str):
    full_tag = f"{repo_name}:{tag}"
    repo = get_aws_repository(full_tag, account_id)
    ecr_login(account_id)
    docker_api_client.tag(full_tag, repo)
    response = docker_api_client.push(repo)
    return response

#takes a single registry id and logs docker into the ECR Registry
def ecr_login(account_id: str):
    ecr_response = ecr_client.get_authorization_token(registryIds=[account_id])
    auth_data = ecr_response['authorizationData'][0]
    decoded_token = base64.b64decode(auth_data['authorizationToken']).decode("utf-8")
    user = decoded_token.split(':')[0]
    password = decoded_token.split(':')[1]
    registry_url = auth_data['proxyEndpoint']

    # Note that you'll always get the "Login Succeeded" response, even if you shouldn't
    # be able to log in to the account.
    docker_response = docker_api_client.login(
        username=user,
        password=password,
        registry=registry_url,
        reauth=True
    )

    # The only way to know if you're login actually succeeded is to try to do 
    # something once you've "logged in".
    ecr_describe_response = ecr_client.describe_repositories(registryId=account_id, maxResults=1)
    return docker_response

def get_aws_repository(full_tag: str, account_id: str) -> str:
    return f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/{full_tag}"


# A function similar to this needs to live in the Transaction job class
# of wherever we're actually defining what needs to run.
# def generate_transaction_job_container_overrides(transaction_id: str, input_contract: str, output_contract: str, env: str):
#     overrides = {
#         'command': [
#             "corebot run_transaction",
#             f"--id={transaction_id}",
#             f"--input_contract={input_contract}",
#             f"--output_contract={output_contract}",
#             f"--env={env}",
#             "--executer=batch"
#         ],
#         'environment': [
#             {
#                 'name': 'AWS_DEFAULT_REGION',
#                 'value': 'us-east-1'
#             },
#         ]
#     }
#     return overrides

# Generate a super basic container_overrides object for running the integration test
def generate_it_test_container_overrides():
    overrides = {
        'command': [
            "--help",
        ],
        'environment': [
            {
                'name': 'AWS_DEFAULT_REGION',
                'value': 'us-east-1'
            },
        ]
    }
    return overrides


def register_job_definition(
    job_def_name: str,
    container_image_uri: str,
    job_role_arn: str = "arn:aws:iam::687531504312:role/ecs-tasks",
    ulimits: list = [],
    timeout: int = 7200,
    vcpus: int = 2,
    memory: int = 2048
):

    response = batch_client.register_job_definition(
        jobDefinitionName=job_def_name,
        type='container',
        containerProperties={
            'image': container_image_uri,
            'vcpus': vcpus,
            'memory': memory,
            'command': [
                'echo hello_world',
            ],
            'jobRoleArn': job_role_arn,
            'ulimits': ulimits,
        },
        retryStrategy={
            'attempts': 2
        },
        timeout={
            'attemptDurationSeconds': 123
        }
    )
    return response

# De-register every revision of a job_def_name
def deregister_job_definition_set(job_def_name: str):
    job_definitions_response = batch_client.describe_job_definitions(jobDefinitionName=job_def_name)
    
    job_defs = job_definitions_response['jobDefinitions']
    responses = []
    for job_def in job_defs:
        name = job_def['jobDefinitionName']
        revision = job_def['revision']
        response = deregister_job_definition(f"{name}:{revision}")
        responses.append(response)

    return responses


def deregister_job_definition(job_def_name_and_revision: str):
    response = batch_client.deregister_job_definition(
        jobDefinition=job_def_name_and_revision
    )
    return response


def launch_batch_job(job_name: str, job_definition: str, job_queue: str, container_overrides: dict):
    response = batch_client.submit_job(
        jobName=job_name,
        jobQueue=job_queue,
        jobDefinition=job_definition,
        containerOverrides=container_overrides
    )
    return response