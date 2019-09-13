#!/bin/bash
# No BS way to get a PROD image on aws
# FOR SANDBOX USE ONLY: the account id is hardcoded to sandbox

# Build image
. ~/Repos/core/script/script_setup
docker-compose build --no-cache airflow;

# Login to aws
GET_LOGIN=$(aws ecr --profile prod get-login --no-include-email)
eval $GET_LOGIN

# Tag the image
docker tag ichain/core:latest 687531504312.dkr.ecr.us-east-1.amazonaws.com/ichain/core

# Push the image
docker push 687531504312.dkr.ecr.us-east-1.amazonaws.com/ichain/core