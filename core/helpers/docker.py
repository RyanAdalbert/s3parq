import docker
from git import Repo
import os

cwd = os.getcwd()
DOCKERFILE_LOCATION = cwd+'/dockerfiles/core.dockerfile'
BASE_DOCKER_TAG = 'ichain/core'

# builds a docker image of the current state of the project and
# tags it with the current git branch.
def build_branch_image() -> str:
    repo = Repo('.')
    branch_name = repo.active_branch.name
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    tag = f"{BASE_DOCKER_TAG}:{branch_name}"
    client.build(path=cwd, dockerfile=DOCKERFILE_LOCATION, tag=tag)

    response = [line for line in client.build(
        path=cwd, dockerfile=DOCKERFILE_LOCATION, rm=True, tag=tag
    )]
    return tag

def push_image(tag: str, arn: str):
    pass