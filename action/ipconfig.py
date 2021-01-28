"""
Exports a `get_ip_config` method, that returns a suitable list for the IpPermissions param on both boto3 methods:
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.revoke_security_group_ingress
"""
import ipaddress
import os
import sys
import urllib.request

from action.logger import logging

lg = logging.getLogger("get-ip-config")


def get_ip_config() -> list:
    env = os.environ
    port_range = env.get("INPUT_PORT_RANGE", "443").split("-")
    ip_string = ""
    try:
        ip_string = get_ip_string()
        external_ip = ipaddress.IPv4Address(ip_string)
    except ipaddress.AddressValueError:
        lg.error(f"The detected '{ip_string}' is not a valid ipv4 address")
        sys.exit(1)
    lg.info(f"Ingress rule with IP '{external_ip}'")
    return [
        {
            "FromPort": int(port_range[0]),
            "ToPort": int(port_range[1] if len(port_range) == 2 else port_range[0]),
            "IpProtocol": "tcp",
            "IpRanges": [
                {
                    "CidrIp": f"{external_ip}/32",
                    "Description": env.get("INPUT_DESCRIPTION"),
                },
            ],
        }
    ]


def get_ip_string() -> str:
    return (
        urllib.request.urlopen("http://checkip.amazonaws.com/")  # nosec
        .read()
        .decode("utf8")[:-1]
    )
