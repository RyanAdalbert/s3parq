import docker
import os

cwd = os.getcwd()
DOCKERFILE_LOCATION = cwd+'/dockerfiles/core.dockerfile'
DOCKER_REPO = 'ichain/core'

docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')

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


def push_image(tag: str, arn: str):
    pass