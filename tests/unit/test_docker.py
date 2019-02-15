import pytest
from core.helpers import docker
from git import Repo
import os
import core.constants as core_constants
from typing import Callable
from unittest.mock import patch

def with_env(env: str, module: str, f: Callable):
    @patch(f"{module}.ENVIRONMENT", env)
    def p_f():
        return f()
    return p_f()

class Test():
    def setup(self):
        self.module = "core.helpers.docker"
        self.starting_env = core_constants.ENVIRONMENT
        self.branch_name = Repo('.').active_branch.name

    def test_get_core_tag(self):
        self.setup()
        dev_tag = with_env("dev", self.module, docker.get_core_tag)
        assert dev_tag == f"ichain/core:{self.branch_name}"

        uat_tag = with_env("uat", self.module, docker.get_core_tag)
        assert uat_tag == "ichain/core:uat"

        prod_tag = with_env("prod", self.module, docker.get_core_tag)
        assert prod_tag == "ichain/core:prod"

    def test_get_core_job_def_name(self):
        self.setup()
        dev_job_def_name = with_env("dev", self.module, docker.get_core_job_def_name)
        assert dev_job_def_name == f"core_{self.branch_name}"

        uat_job_def_name = with_env("uat", self.module, docker.get_core_job_def_name)
        assert uat_job_def_name == f"core_uat"

        prod_job_def_name = with_env("prod", self.module, docker.get_core_job_def_name)
        assert prod_job_def_name == f"core_prod"

    def test_get_aws_account(self):
        self.setup()
        dev_aws_account = with_env("dev", self.module, docker.get_aws_account)
        assert dev_aws_account == "265991248033"

        uat_aws_account = with_env("uat", self.module, docker.get_aws_account)
        assert uat_aws_account == "687531504312"

        prod_aws_account = with_env("prod", self.module, docker.get_aws_account)
        assert prod_aws_account == "687531504312"

    def test_get_aws_tag(self):
        tag = docker.get_aws_tag("core_test", "123456789012")
        assert tag == "123456789012.dkr.ecr.us-east-1.amazonaws.com/core_test"