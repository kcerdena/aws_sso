import pytest
import boto3
from botocore.stub import Stubber


@pytest.fixture(autouse=True)
def sso_stub():
    sso = boto3.client('sso')
    with Stubber(sso) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()