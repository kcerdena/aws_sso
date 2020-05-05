import pytest
import pytest_mock
from aws_sso import file_handler


def test_get_file_contents():
    file_handler.get_file_contents('~/.aws/config')

    

