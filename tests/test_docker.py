import moto
import pytest
import docker
from docker.models.images import Image
from docker.errors import ImageNotFound
from core.helpers import docker as core_docker

docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def test_build_core_image():
    # images = docker_client.images.list()
    # for image in images:
    #     print(image.tags)
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

# def test_get_aws_repository():
#     full_tag = "test/unit:latest"
#     account_id = "1234567890"
#     assert get_aws_repository(full_tag, account_id) == "1234567890.dkr.ecr.us-east-1.amazonaws.com/test/unit:latest"