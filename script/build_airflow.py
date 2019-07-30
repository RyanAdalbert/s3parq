from core.helpers.docker import CoreDocker as cd
from core.constants import DEV_AWS_ACCOUNT

airflow = cd()

tag = "ichain/core:airflow-simple"

airflow.build_image(tag)
airflow.register_image(tag, DEV_AWS_ACCOUNT)