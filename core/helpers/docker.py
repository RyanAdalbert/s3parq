import boto3
import docker
import base64
import os
from core.constants import AWS_ACCOUNT, AWS_REGION, DEV_AWS_ACCOUNT, PROD_AWS_ACCOUNT, DOCKER_REPO, ENVIRONMENT
from core.helpers.project_root import ProjectRoot
from core.logging import LoggerMixin
from git import Repo

# In jenkins there isn't a branch name since the code is checked out via
# commit hash, the work-around is to use the BRANCH_NAME env var that
# Jenkins sets.
def get_branch_name():
    repo = Repo(ProjectRoot().get_path())
    try:
        return repo.active_branch.name
    except:
        return os.environ['BRANCH_NAME']

def get_core_tag():
    print(ENVIRONMENT)
    if ENVIRONMENT == 'dev':
        branch_name = get_branch_name()
        return f"{DOCKER_REPO}:{branch_name}"
    elif ENVIRONMENT == 'uat':
        return f"{DOCKER_REPO}:uat"
    elif ENVIRONMENT == 'prod':
        return f"{DOCKER_REPO}:prod"
    else:
        raise Exception(f"Can't create a core tag for environment {ENVIRONMENT}")


def get_core_job_def_name():
    if ENVIRONMENT == 'dev':
        branch_name = get_branch_name()
        return f"core_{branch_name}"
    elif ENVIRONMENT == 'uat':
        return "core_uat"
    elif ENVIRONMENT == 'prod':
        return "core_prod"    
    else:
        raise Exception(f"Can't create a core tag job definition name for environment {ENVIRONMENT}")

def get_aws_account():
    if ENVIRONMENT == 'dev':
        return DEV_AWS_ACCOUNT
    elif ENVIRONMENT == 'uat':
        return PROD_AWS_ACCOUNT
    elif ENVIRONMENT == 'prod':
        return PROD_AWS_ACCOUNT
    else:
        raise Exception(f"Can't find an AWS account id for environment {ENVIRONMENT}")

def get_aws_tag(tag: str, account_id: str) -> str:
    """ returns the url for the aws repository. """
    return f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/{tag}"


class CoreDocker(LoggerMixin):
    # Note, that in this library the variable name "tag" comes from docker terms
    # and contains both the repo name `ichain/core` and the branch (`prod`, `uat`, 
    # `DC-123-something_great`).

    def __init__(self):
        self.p_root = ProjectRoot().get_path()
        self.CORE_DOCKERFILE_LOCATION = os.path.join(self.p_root,
                                                            'dockerfiles',
                                                            'core.dockerfile')
        self.batch_client = boto3.client('batch')
        self.ecr_client = boto3.client('ecr')
        self.d_api_client = self._build_docker_api_client()
        self.d_client = self._build_docker_client()

    def _build_docker_api_client(self) -> docker.APIClient:
        return docker.APIClient(base_url='unix://var/run/docker.sock')

    def _build_docker_client(self) -> docker.DockerClient:
        return docker.DockerClient(base_url='unix://var/run/docker.sock')

    def build_image(self, tag: str) -> str:
        """ builds and tags an image of the current state of the repo."""
        d_client = self._build_docker_api_client()
        #TODO: Need to figure out a way to see see that this image didn't fail building
        self.logger.debug(f"Building {tag} from {self.CORE_DOCKERFILE_LOCATION} with context {self.p_root}")
        response = [line for line in d_client.build(
            path=self.p_root, dockerfile=self.CORE_DOCKERFILE_LOCATION, rm=True, tag=tag
        )]
        return tag

    def remove_image(self, tag: str):
        response = self.d_api_client.remove_image(tag)
        return response

    def remove_ecr_image(self, tag: str, repo_name: str, account_id: str):
        self._ecr_login(account_id)
        tag_without_repo = ":".join(tag.split(':')[1:])
        aws_tag = get_aws_tag(tag, account_id)
        image = self.d_client.images.get(aws_tag)
        repo_digest = image.attrs['RepoDigests'][0]
        digest_sha = repo_digest.split("@")[-1]

        # remove the image from ECR
        response = self.ecr_client.batch_delete_image(
            registryId=account_id,
            repositoryName=repo_name,
            imageIds=[
                {
                    'imageDigest': digest_sha,
                    'imageTag': tag_without_repo
                },
            ]
        )
        # remove the dev image
        self.d_api_client.remove_image(aws_tag)
        return response

    def register_image(self, tag: str, repo_name: str, account_id: str):
        repo_name = tag.split(':')[0]
        aws_tag = get_aws_tag(tag, account_id)
        self._ecr_login(account_id)
        self.d_api_client.tag(tag, aws_tag)
        response = self.d_api_client.push(aws_tag)
        return response

    def _ecr_login(self, account_id: str):
        """ logs docker into the ecr Registry using the given account id."""
        ecr_response = self.ecr_client.get_authorization_token(registryIds=[account_id])
        auth_data = ecr_response['authorizationData'][0]
        decoded_token = base64.b64decode(auth_data['authorizationToken']).decode("utf-8")
        user = decoded_token.split(':')[0]
        password = decoded_token.split(':')[1]
        registry_url = auth_data['proxyEndpoint']

        # Note that you'll always get the "Login Succeeded" response, even if you shouldn't
        # be able to log in to the account.

        docker_response = self.d_api_client.login(
            username=user,
            password=password,
            registry=registry_url,
            reauth=True
        )

        # The only way to know if you're login actually succeeded is to try to do 
        # something once you've "logged in".
        ecr_describe_response = self.ecr_client.describe_repositories(registryId=account_id, maxResults=1)
        return docker_response


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
        response = self.batch_client.register_job_definition(
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

    def deregister_job_definition_set(self, job_def_name: str):
        """De-register every revision of a job_def_name"""
        job_definitions_response = self.batch_client.describe_job_definitions(jobDefinitionName=job_def_name)
        
        job_defs = job_definitions_response['jobDefinitions']
        responses = []
        for job_def in job_defs:
            name = job_def['jobDefinitionName']
            revision = job_def['revision']
            response = self.deregister_job_definition(f"{name}:{revision}")
            responses.append(response)

        return responses


    def deregister_job_definition(self, job_def_name_and_revision: str):
        response = self.batch_client.deregister_job_definition(
            jobDefinition=job_def_name_and_revision
        )
        return response


    def launch_batch_job(self, job_name: str, job_definition: str, job_queue: str, container_overrides: dict):
        response = self.batch_client.submit_job(
            jobName=job_name,
            jobQueue=job_queue,
            jobDefinition=job_definition,
            containerOverrides=container_overrides
        )
        return response

