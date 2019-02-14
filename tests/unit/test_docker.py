import pytest
from core.helpers import docker
from git import Repo
from core.helpers.project_root import ProjectRoot

class Test():
    def setup(self):
        self.branch_name = Repo(ProjectRoot().get_path()).active_branch.name

    def test_get_core_tag(self):
        self.setup()
        local_tag = docker.get_core_tag("local")
        uat_tag = docker.get_core_tag("uat")
        prod_tag = docker.get_core_tag("prod")

        assert local_tag == f"ichain/core:{self.branch_name}"
        assert uat_tag == "ichain/core:uat"
        assert prod_tag == "ichain/core:prod"

        with pytest.raises(Exception):
            docker.get_core_tag("hemoglobin")

    def test_get_core_job_def_name(self):
        self.setup()
        local_job_def_name = docker.get_core_job_def_name("local")
        uat_job_def_name = docker.get_core_job_def_name("uat")
        prod_job_def_name = docker.get_core_job_def_name("prod")

        assert local_job_def_name == f"core_{self.branch_name}"
        assert uat_job_def_name == f"core_uat"
        assert prod_job_def_name == f"core_prod"

        with pytest.raises(Exception):
            docker.get_core_job_def_name("hemoglobin")

    def test_get_aws_account(self):
        local_aws_account = docker.get_aws_account("local")
        uat_aws_account = docker.get_aws_account("uat")
        prod_aws_account = docker.get_aws_account("prod")

        assert local_aws_account == "265991248033"
        assert uat_aws_account == "687531504312"
        assert prod_aws_account == "687531504312"

        with pytest.raises(Exception):
            docker.get_aws_account("hemoglobin")

    def test_get_aws_tag(self):
        tag = docker.get_aws_tag("core_test", "123456789012")
        assert tag == "123456789012.dkr.ecr.us-east-1.amazonaws.com/core_test"