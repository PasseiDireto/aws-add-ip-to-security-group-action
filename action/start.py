"""
Add a TCP Ingress rule to a AWS Security Group
"""
import os

import boto3

from .ipconfig import get_ip_config
from .logger import logging

logger = logging.getLogger("create-ingress-rule")


def start():
    client = boto3.client("ec2")
    response = client.authorize_security_group_ingress(
        GroupId=os.getenv("INPUT_AWS_SECURITY_GROUP_IDS"), IpPermissions=get_ip_config()
    )
    print(response)


if __name__ == "__main__":
    start()
