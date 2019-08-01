# Running this script is a quick way to register the current local core.dockerfile image to AWS ECR

from core.helpers.docker import CoreDocker as cd
from core.constants import DEV_AWS_ACCOUNT

docker = cd()

# Keep ichain/core: as it is the ECR repository our images live in
tag = "ichain/core:core-airflow"

docker.build_image(tag)
docker.register_image(tag, DEV_AWS_ACCOUNT)