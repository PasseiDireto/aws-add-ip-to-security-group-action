"""
Add a TCP Ingress rule to a AWS Security Group
"""
import os
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError, ParamValidationError

from action.ipconfig import get_ip_config
from action.logger import logging

lg = logging.getLogger("create-ingress-rule")


def start():
    client = boto3.client("ec2")
    lg.info("Creating ingress rule")
    try:
        client.authorize_security_group_ingress(
            GroupId=os.getenv("INPUT_AWS_SECURITY_GROUP_IDS"),
            IpPermissions=get_ip_config(),
        )
    except (ClientError, ParamValidationError) as e:
        lg.error(
            "Something went wrong with the request. Check the inputs you provided."
        )
        lg.error(e)
        sys.exit(1)
    except BotoCoreError as e:
        lg.error(
            "AWS API returned could not fulfill the request. Check you credentials and try again"
        )
        lg.error(e)
        sys.exit(1)


if __name__ == "__main__":
    start()
