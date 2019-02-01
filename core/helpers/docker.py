import boto3
import docker
import base64
from core.constants import AWS_ACCOUNT, AWS_REGION


class CoreDocker:

    def __init__(self):
        self.CORE_DOCKERFILE_LOCATION = f'{ProjectRoot().get_path()}/dockerfiles/core.dockerfile'
        batch_client = boto3.client('batch')

    def _build_docker_api_client(self) -> docker.APIClient:
        return docker.APIClient(base_url='unix://var/run/docker.sock')

    def _build_docker_client(self) -> docker.DockerClient:
        return docker.DockerClient(base_url='unix://var/run/docker.sock')

    def build_image(full_tag: str) -> str:
        """ builds and tags an image of the current state of the repo."""
        d_client = self._build_docker_api_client()
        #TODO: Need to figure out a way to see see that this image didn't fail building
        response = [line for line in d_client.build(
            path=cwd, dockerfile=CORE_DOCKERFILE_LOCATION, rm=True, tag=full_tag
        )]
        return full_tag

    def remove_image(self,full_tag: str):
        #Note to self: do we actually do anything with the images here? 
        ###d_client = self._build_docker_client()
        d_api_client = self._build_docker_api_client()
        ###image = d_client.images.get(full_tag)
        response = d_api_client.remove_image(full_tag)
        return response

    def remove_ecr_image(self,tag: str, repo_name: str, account_id: str):
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
        docker_api_client.remove_image(self,ecr_tagged_image_name)
        return response

    def register_image(self,tag: str, repo_name: str, account_id: str):
        full_tag = f"{repo_name}:{tag}"
        repo = get_aws_repository(full_tag, account_id)
        ecr_login(account_id)
        docker_api_client.tag(full_tag, repo)
        response = docker_api_client.push(repo)
        return response

    def _ecr_login(self,account_id: str):
        """ logs docker into the ecr Registry using the given account id."""
        ecr_client = boto3.client('ecr')
        ecr_response = ecr_client.get_authorization_token(registryIds=[account_id])
        auth_data = ecr_response['authorizationData'][0]
        decoded_token = base64.b64decode(auth_data['authorizationToken']).decode("utf-8")
        user = decoded_token.split(':')[0]
        password = decoded_token.split(':')[1]
        registry_url = auth_data['proxyEndpoint']

        # Note that you'll always get the "Login Succeeded" response, even if you shouldn't
        # be able to log in to the account.
        docker_response = self._docker_api_client().login(
            username=user,
            password=password,
            registry=registry_url,
            reauth=True
        )

        # The only way to know if you're login actually succeeded is to try to do 
        # something once you've "logged in".
        ecr_describe_response = ecr_client.describe_repositories(registryId=account_id, maxResults=1)
        return docker_response

    def get_aws_repository(self,full_tag: str, account_id: str) -> str:
        """ returns the url for the aws repository. """
        return f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/{full_tag}"

    def register_job_definition(self,
        job_def_name: str,
        container_image_uri: str,
        job_role_arn: str = f"arn:aws:iam::{AWS_ACCOUNT}:role/ecs-tasks",
        ulimits: list = [],
        timeout: int = 7200,
        vcpus: int = 2,
        memory: int = 2048
    ):

        # Note that the command will be overwritten with the
        # container_overrides on launch.
        batch_client = boto3.client('batch')
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
                'environment': [
                    {
                        'name': 'AWS_DEFAULT_REGION',
                        'value': AWS_REGION
                    }
                ],
                'jobRoleArn': job_role_arn,
                'ulimits': ulimits,
            },
            retryStrategy={
                'attempts': 2
            },
            timeout={
                'attemptDurationSeconds': timeout
            }
        )
        return response

    def deregister_job_definition_set(self,job_def_name: str):
        """De-register every revision of a job_def_name"""
        batch_client = boto3.client('batch')
        job_definitions_response = batch_client.describe_job_definitions(jobDefinitionName=job_def_name)
        
        job_defs = job_definitions_response['jobDefinitions']
        responses = []
        for job_def in job_defs:
            name = job_def['jobDefinitionName']
            revision = job_def['revision']
            response = deregister_job_definition(f"{name}:{revision}")
            responses.append(response)

        return responses


    def deregister_job_definition(self, job_def_name_and_revision: str):
        batch_client = boto3.client('batch')
        response = batch_client.deregister_job_definition(
            jobDefinition=job_def_name_and_revision
        )
        return response


    def launch_batch_job(self,job_name: str, job_definition: str, job_queue: str, container_overrides: dict):
        batch_client = boto3.client('batch')
        response = batch_client.submit_job(
            jobName=job_name,
            jobQueue=job_queue,
            jobDefinition=job_definition,
            containerOverrides=container_overrides
        )
        return response
