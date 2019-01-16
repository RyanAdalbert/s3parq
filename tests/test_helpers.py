import pytest
import os
from core.helpers.project_root import ProjectRoot

def test_project_root_in_project():
    root = ProjectRoot()
    assert isinstance(root.get_path(), str)
    assert isinstance(root.__str__(),str)  

def test_project_root_not_in_project():
    os.chdir('/')
    root = ProjectRoot()
    assert root.get_path() is False
