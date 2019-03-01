import pytest
import docker
import boto3
from datetime import datetime, timezone, timedelta
import time

from docker.models.images import Image
from docker.errors import ImageNotFound
from core.helpers.docker import CoreDocker
from core.helpers import docker as c_docker
from botocore.exceptions import ClientError
from core.constants import AWS_ACCOUNT, DOCKER_REPO, AWS_BATCH_TEST_JOB_QUEUE

class Test:

    def setup(self):
        self.docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.ecr_client = boto3.client('ecr')
        self.core_docker = CoreDocker()
        self.AWS_BATCH_TEST_JOB_QUEUE = AWS_BATCH_TEST_JOB_QUEUE

    # Generate a super basic container_overrides object for running the integration test
    def generate_it_test_container_overrides(self):
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

    def test_integration_docker(self):
        self.setup()
        tag_without_repo = "it_test"
        new_tag_without_repo = "it_test_retagged"
        job_def_name = "core_it_test"

        #   1. Build the image
        tag = self.core_docker.build_image(f"{DOCKER_REPO}:{tag_without_repo}")
        test_image = self.docker_client.images.get(tag)

        #   2. Log into ECR
        with pytest.raises(ClientError):
            self.core_docker._ecr_login("123456789012")
        self.core_docker._ecr_login(AWS_ACCOUNT)

        #   3. Push the image to ECR
        self.core_docker.register_image(tag, AWS_ACCOUNT)
        aws_tag = c_docker.get_aws_tag(tag, AWS_ACCOUNT)
        test_ecr_image = self.docker_client.images.get(aws_tag)
        assert type(test_ecr_image) is Image

        try:
            repo_digest = test_ecr_image.attrs['RepoDigests'][0]
        except:
            time.sleep(10)
            repo_digest = test_ecr_image.attrs['RepoDigests'][0]

        digest_sha = repo_digest.split("@")[-1]

        ecr_resp = self.ecr_client.describe_images(
            registryId=AWS_ACCOUNT,
            repositoryName=DOCKER_REPO,
            imageIds=[
                {
                    'imageDigest': digest_sha,
                    'imageTag': tag_without_repo
                }
            ]
        )

        # Make sure the image got pushed in a timely manner
        assert tag_without_repo in ecr_resp['imageDetails'][0]['imageTags']
        time_since_image_pushed = datetime.now(timezone.utc) - ecr_resp['imageDetails'][0]['imagePushedAt']
        assert timedelta(minutes=5) > time_since_image_pushed


        # Retag the image and make sure it's there.
        new_tag = f"{DOCKER_REPO}:{new_tag_without_repo}"
        self.core_docker.add_tag_in_ecr(tag, new_tag, AWS_ACCOUNT)

        # grab the existing digest since we're just retagging, not rebuilding
        try:
            repo_digest = test_ecr_image.attrs['RepoDigests'][0]
        except:
            time.sleep(10)
            repo_digest = test_ecr_image.attrs['RepoDigests'][0]
        digest_sha = repo_digest.split("@")[-1]

        ecr_resp = self.ecr_client.describe_images(
            registryId=AWS_ACCOUNT,
            repositoryName=DOCKER_REPO,
            imageIds=[
                {
                    'imageDigest': digest_sha,
                    'imageTag': new_tag_without_repo
                }
            ]
        )
        assert new_tag_without_repo in ecr_resp['imageDetails'][0]['imageTags']


        #   4. Register a Job Definition on Batch
        rjd_resp = self.core_docker.register_job_definition(
            job_def_name,
            aws_tag
        )

        #   5. Launch a Job on Batch
        # Note that this test doesn't check to see if the job run finishes!
        # The api request will go through, however the actual batch
        # job will fail because by the time Batch wants to run the container
        # its definition has already been removed.
        # CannotPullContainerError: API error (404): manifest for 687531504312.dkr.ecr.us-east-1.amazonaws.com/ichain/core:it_test not found
        container_overrides = self.generate_it_test_container_overrides()
        self.core_docker.launch_batch_job("it_test", job_def_name, self.AWS_BATCH_TEST_JOB_QUEUE, container_overrides)

        #   6. Deregister Job Definiton
        self.core_docker.deregister_job_definition_set(job_def_name)

        #   7. Remove images from ECR
        self.core_docker.remove_ecr_image(tag, AWS_ACCOUNT)
        self.core_docker.remove_ecr_image(new_tag, AWS_ACCOUNT)

        #   8. Remove image from your machine
        self.core_docker.remove_image(tag)
        with pytest.raises(ImageNotFound):
            self.docker_client.images.get(tag)
