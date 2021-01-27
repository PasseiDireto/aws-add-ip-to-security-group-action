"""
Exports a `get_ip_config` method, that returns a suitable list for the IpPermissions param on both boto3 methods:
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.revoke_security_group_ingress
"""
import os
import urllib.request


def get_ip_config() -> list:
    env = os.environ
    print(env)
    port_range = env.get("INPUT_PORT_RANGE", "443").split("-")
    external_ip = (
        urllib.request.urlopen("http://checkip.amazonaws.com/")  # nosec
        .read()
        .decode("utf8")[:-1]
    )
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
