from verses.aws.base import Object

from ..base import filters
from .base import client


def query(cls, filters=None):
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    - https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/APIReference/API_DescribeInstances.html
    """
    q = filters and dict(Filters=filters) or {}
    return Object(client().describe_instances(**q))


def query_by_name(cls, name):
    res = query(cls, filters=filters(("Name", name)))
    return res.Reservations[0].Instances[0] if len(res.Reservations) == 1 else None


def tag_specifications(res_type, keyvalues):
    return [
        {
            "ResourceType": res_type,
            "Tags": [{"Key": key, "Value": value} for key, value in keyvalues.items()],
        }
    ]
