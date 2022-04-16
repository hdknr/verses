import boto3

from ..base import call, to_tags


def client():
    return boto3.client("ec2")


def resource():
    return boto3.resource("ec2")


def delete_tags(resources, tags, resource_type=None, dry_run=False):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_tags
    kwargs = dict(
        Resources=resources,
        DryRun=dry_run,
    )
    if tags:
        kwargs["Tags"]=to_tags(tags)

    print(kwargs)
    return call(client().delete_tags, **kwargs)
