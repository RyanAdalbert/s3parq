import pytest
from core.helpers import docker
from core.constants import BRANCH_NAME
import os
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