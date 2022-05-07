from .. import base
from .base import client


def query_by_name(cls, name, raw=False):
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    - https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/APIReference/API_DescribeInstances.html
    """
    filters = base.filters({"Name": name}, {"instance-state-code": "16"})  # only running
    res = base.describe(None, client().describe_instances, filters=filters, raw=raw)

    if raw and len(res["Reservations"]) > 0:
        return res["Reservations"][0]["Instances"][0]

    return res.Reservations[0].Instances[0] if len(res.Reservations) > 0 else None
