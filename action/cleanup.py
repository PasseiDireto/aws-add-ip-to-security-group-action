"""
Revoke the freshly created security group ingress rule after workflow termination
"""
import os

import boto3

from action.ipconfig import get_ip_config
from action.logger import logging

logger = logging.getLogger("cleanup-ingress-rule")


def cleanup():
    client = boto3.client("ec2")
    response = client.revoke_security_group_ingress(
        GroupId=os.getenv("INPUT_AWS_SECURITY_GROUP_IDS"), IpPermissions=get_ip_config()
    )
    print(response)


if __name__ == "__main__":
    cleanup()
