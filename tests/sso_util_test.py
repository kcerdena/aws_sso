import pytest
import subprocess
from aws_sso import sso_util


def test_exec_login():
    sso_util.exec_login('testProfile')
    
