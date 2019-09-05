#!/bin/bash
# No BS way to get an image on aws
# FOR SANDBOX USE ONLY: the account id is hardcoded to sandbox

# Build image
. ~/Repos/core/script/script_setup
docker-compose build --no-cache airflow;

#### SET THE TAG HERE ####
TAG="ichain/core:corebot-batch"
#TAG="ichain/core:airflow"

# Login to aws
GET_LOGIN=$(aws ecr get-login --no-include-email --region us-east-1)
eval $GET_LOGIN

# Tag the image
docker tag ichain/core:latest 265991248033.dkr.ecr.us-east-1.amazonaws.com/${TAG}

# Push the image
docker push 265991248033.dkr.ecr.us-east-1.amazonaws.com/${TAG}
