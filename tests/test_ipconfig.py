import os

import mock
import pytest

import action.ipconfig as ipconfig


@pytest.fixture()
def env():
    os.environ["INPUT_AWS_SECURITY_GROUP_IDS"] = "sg123"
    os.environ["INPUT_PORT_RANGE"] = "6622"
    os.environ["INPUT_DESCRIPTION"] = "Test Rule"


@mock.patch("action.ipconfig.get_ip_string", return_value="192.168.1.1")
def test_get_ip_ok(patch, env):
    config = ipconfig.get_ip_config()[0]
    assert config["FromPort"] == 6622
    assert config["ToPort"] == 6622
    assert config["IpRanges"][0]["CidrIp"] == "192.168.1.1/32"
    assert config["IpRanges"][0]["Description"] == "Test Rule"


@mock.patch("action.ipconfig.get_ip_string", return_value="192.168.1.1")
def test_get_ip_ok_range(patch, env):
    os.environ["INPUT_PORT_RANGE"] = "6622-6644"
    config = ipconfig.get_ip_config()[0]
    assert config["FromPort"] == 6622
    assert config["ToPort"] == 6644


@mock.patch("action.ipconfig.get_ip_string", return_value="192.168.1.x32")
def test_get_ip_invalid_address(patch, env):
    with pytest.raises(SystemExit):
        ipconfig.get_ip_config()
