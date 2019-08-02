import pytest
from core.aws import docker
from core.constants import BRANCH_NAME
import os
from typing import Callable
from unittest.mock import patch
from core.helpers.project_root import ProjectRoot


def with_env(env: str, module: str, f: Callable):
    @patch(f"{module}.ENVIRONMENT", env)
    def p_f():
        return f()
    return p_f()


class Test():
    def setup(self):
        self.module = "core.aws.docker"

    def test_get_core_tag(self):
        self.setup()
        dev_tag = with_env("dev", self.module, docker.get_core_tag)
        assert dev_tag == f"ichain/core:{BRANCH_NAME}"

        uat_tag = with_env("uat", self.module, docker.get_core_tag)
        assert uat_tag == "ichain/core:uat"

        prod_tag = with_env("prod", self.module, docker.get_core_tag)
        assert prod_tag == "ichain/core:prod"

        with pytest.raises(Exception):
            with_env("invalid_environment", self.module, docker.get_core_tag)

    def test_get_aws_account(self):
        self.setup()
        dev_aws_account = with_env("dev", self.module, docker.get_aws_account)
        assert dev_aws_account == "265991248033"

        uat_aws_account = with_env("uat", self.module, docker.get_aws_account)
        assert uat_aws_account == "687531504312"

        prod_aws_account = with_env(
            "prod", self.module, docker.get_aws_account)
        assert prod_aws_account == "687531504312"

        with pytest.raises(Exception):
            with_env("invalid_environment", self.module,
                     docker.get_aws_account)

    def test_get_aws_tag(self):
        tag = docker.get_aws_tag("core_test", "123456789012")
        assert tag == "123456789012.dkr.ecr.us-east-1.amazonaws.com/core_test"
