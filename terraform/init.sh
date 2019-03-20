#!/bin/bash

tf_region="us-east-1"
tf_service_name=${1}
tf_environment="sandbox"

terraform init -backend=true \
    -backend-config="bucket=ichain-terraform" \
    -backend-config="key=${tf_environment}/${tf_service_name}.tfstate" \
    -backend-config="region=${tf_region}" \
    -backend-config="encrypt=true"

if [ -f "terraform.tfvars" ]; then
    echo "File: terraform.tfvars exists! I won't modify the file but you should check to make sure the values are correct."
else
    echo "Generating terraform.tfvars"
    echo "service_name = \"${tf_service_name}\"" > terraform.tfvars
fi
