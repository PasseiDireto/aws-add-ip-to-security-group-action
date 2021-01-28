import os

import boto3
import mock
import pytest
from moto import mock_ec2

from action.cleanup import cleanup
from action.start import start


@pytest.fixture(scope="function")
def env():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # nosec
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["INPUT_PORT_RANGE"] = "6622"
    os.environ["INPUT_DESCRIPTION"] = "Test Rule"


@mock.patch("action.ipconfig.get_ip_string", return_value="192.168.1.1")
def test_add_revoke_ok(patch, env):
    with mock_ec2():
        ec2 = boto3.client("ec2")
        sg = ec2.create_security_group(GroupName="testsg", Description="A")
        os.environ["INPUT_AWS_SECURITY_GROUP_IDS"] = sg["GroupId"]
        start()
        cleanup()


@mock.patch("action.ipconfig.get_ip_string", return_value="192.168.1.1xx")
def test_add_invalid_ip(patch, env):
    with mock_ec2():
        ec2 = boto3.client("ec2")
        sg = ec2.create_security_group(GroupName="testsg", Description="A")
        os.environ["INPUT_AWS_SECURITY_GROUP_IDS"] = sg["GroupId"]
        with pytest.raises(SystemExit):
            start()


@mock.patch("action.ipconfig.get_ip_string", return_value="192.168.1.1")
def test_add_revoke_not_found(patch, env):
    with mock_ec2():
        cleanup()
