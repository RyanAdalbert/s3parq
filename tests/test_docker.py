import moto
import pytest
import docker
import boto3
from datetime import datetime, timezone, timedelta

from docker.models.images import Image
from docker.errors import ImageNotFound
from core.helpers import docker as core_docker
from botocore.exceptions import ClientError

docker_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
ecr_client = boto3.client('ecr')

AWS_ACCOUNT_ID = "687531504312"

def test_build_core_image():
    full_tag = core_docker.build_image("ichain/core:unit_test")
    test_image = docker_client.images.get(full_tag)
    assert type(test_image) is Image


def test_remove_core_image():
    full_tag = core_docker.build_image("unit_test")
    test_image = docker_client.images.get(full_tag)
    assert type(test_image) is Image

    core_docker.remove_image(full_tag)
    with pytest.raises(ImageNotFound):
        docker_client.images.get(full_tag)

def test_ecr_login():
    core_docker.ecr_login(AWS_ACCOUNT_ID)

    with pytest.raises(ClientError):
        core_docker.ecr_login("123456789012")

# Wonder if this test could basically replace all the others above
# as it's basically an integration test where all the above are run.
def test_register_image():
    REPO_NAME = "ichain/core"
    TAG = "unit_test"
    full_tag = core_docker.build_image(f"{REPO_NAME}:{TAG}")
    test_image = docker_client.images.get(full_tag)

    core_docker.ecr_login(AWS_ACCOUNT_ID)
    core_docker.register_image(TAG, REPO_NAME, AWS_ACCOUNT_ID)

    ecr_tagged_image_name = core_docker.get_aws_repository(full_tag, AWS_ACCOUNT_ID)
    test_ecr_image = docker_client.images.get(ecr_tagged_image_name)

    repo_digest = test_ecr_image.attrs['RepoDigests'][0]
    digest_sha = repo_digest.split("@")[-1]

    ecr_resp = ecr_client.describe_images(
        registryId=AWS_ACCOUNT_ID,
        repositoryName=REPO_NAME,
        imageIds=[
            {
                'imageDigest': digest_sha,
                'imageTag': TAG
            }
        ]
    )

    # Make sure the unit_test image got pushed in a timely manner
    assert TAG in ecr_resp['imageDetails'][0]['imageTags']
    time_since_image_pushed = datetime.now(timezone.utc) - ecr_resp['imageDetails'][0]['imagePushedAt']
    assert timedelta(minutes=5) > time_since_image_pushed

    # Clean up the image
    core_docker.remove_ecr_image(TAG, REPO_NAME, AWS_ACCOUNT_ID)
    core_docker.remove_image(full_tag)