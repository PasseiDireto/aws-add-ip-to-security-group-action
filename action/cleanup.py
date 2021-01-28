"""
Revoke the freshly created security group ingress rule after workflow termination
"""
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from action.ipconfig import get_ip_config
from action.logger import logging

lg = logging.getLogger("cleanup-ingress-rule")


def cleanup():
    client = boto3.client("ec2")
    try:
        lg.info("Removing freshly created ingress rule")
        client.revoke_security_group_ingress(
            GroupId=os.getenv("INPUT_AWS_SECURITY_GROUP_IDS"),
            IpPermissions=get_ip_config(),
        )
    except (BotoCoreError, ClientError) as e:
        lg.warning(
            "The revoke request was not successful. You will need to perform it manually"
        )
        lg.warning(e)


if __name__ == "__main__":
    cleanup()
