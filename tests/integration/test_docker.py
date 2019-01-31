import moto
import pytest
import docker
import boto3
from datetime import datetime, timezone, timedelta

from docker.models.images import Image
from docker.errors import ImageNotFound
from core.helpers import docker as core_docker
from botocore.exceptions import ClientError
from core.constants import AWS_ACCOUNT, DOCKER_REPO

docker_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
ecr_client = boto3.client('ecr')

AWS_BATCH_TEST_JOB_QUEUE = "core"

# Generate a super basic container_overrides object for running the integration test
def generate_it_test_container_overrides():
    overrides = {
        'command': [
            "corecli --help",
        ],
        'environment': [
            {
                'name': 'AWS_DEFAULT_REGION',
                'value': 'us-east-1'
            },
        ]
    }
    return overrides

# This test goes through the whole lifecycle of a docker container used for
# development
#   1. Build the image
#   2. Log into ECR
#   3. Push the image to ECR
#   4. Register a Job Definition on Batch
#   5. Launch a Job on Batch
#   6. Deregister Job Definiton
#   7. Remove image from ECR
#   8. Remove image from your machine

def test_integration_docker():
    TAG = "it_test"

    #   1. Build the image
    full_tag = core_docker.build_image(f"{DOCKER_REPO}:{TAG}")
    test_image = docker_client.images.get(full_tag)

    #   2. Log into ECR
    with pytest.raises(ClientError):
        core_docker.ecr_login("123456789012")
    core_docker.ecr_login(AWS_ACCOUNT)

    #   3. Push the image to ECR
    core_docker.register_image(TAG, DOCKER_REPO, AWS_ACCOUNT)
    ecr_tagged_image_name = core_docker.get_aws_repository(full_tag, AWS_ACCOUNT)
    test_ecr_image = docker_client.images.get(ecr_tagged_image_name)
    assert type(test_ecr_image) is Image

    repo_digest = test_ecr_image.attrs['RepoDigests'][0]
    digest_sha = repo_digest.split("@")[-1]
    ecr_resp = ecr_client.describe_images(
        registryId=AWS_ACCOUNT,
        repositoryName=DOCKER_REPO,
        imageIds=[
            {
                'imageDigest': digest_sha,
                'imageTag': TAG
            }
        ]
    )

    # Make sure the image got pushed in a timely manner
    assert TAG in ecr_resp['imageDetails'][0]['imageTags']
    time_since_image_pushed = datetime.now(timezone.utc) - ecr_resp['imageDetails'][0]['imagePushedAt']
    assert timedelta(minutes=5) > time_since_image_pushed

    #   4. Register a Job Definition on Batch
    rjd_resp = core_docker.register_job_definition(
        "it_test_core",
        ecr_tagged_image_name,
        job_role_arn=f"arn:aws:iam::{AWS_ACCOUNT}:role/ecs-tasks"
    )

    #   5. Launch a Job on Batch
    # Note that this test doesn't check to see if the job run finishes!
    # The api request will go through, however the actual batch
    # job will fail because by the time Batch wants to run the container
    # its definition has already been removed.
    # CannotPullContainerError: API error (404): manifest for 687531504312.dkr.ecr.us-east-1.amazonaws.com/ichain/core:it_test not found
    container_overrides = generate_it_test_container_overrides()
    core_docker.launch_batch_job("it_test", "it_test_core", AWS_BATCH_TEST_JOB_QUEUE, container_overrides)

    #   6. Deregister Job Definiton
    core_docker.deregister_job_definition_set("it_test_core")

    #   7. Remove image from ECR
    core_docker.remove_ecr_image(TAG, DOCKER_REPO, AWS_ACCOUNT)

    #   8. Remove image from your machine
    core_docker.remove_image(full_tag)
    with pytest.raises(ImageNotFound):
        docker_client.images.get(full_tag)
