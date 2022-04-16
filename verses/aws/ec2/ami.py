import click

from verses.aws import base
from verses.base import logs

from ..base import keyvalues, filters, to_value
from .base import client, delete_tags


def remove_tags(searching: dict, exclude_ids=None, removing: dict = None):
    exclude_ids = exclude_ids or []
    res = base.describe(
        None,
        client().describe_images,
        filters=filters(searching, {}),
    )
    resources = [image.ImageId for image in res.Images if image.ImageId not in exclude_ids]
    if resources:
        return delete_tags(resources, removing)


def to_values(data, fields):
    data = dict((i, to_value(data, i)) for i in fields)
    tags = data.get("Tags", None) or []
    data["Tags"] = dict((to_value(i, "Key"), to_value(i, "Value")) for i in tags)
    return data


def find(tags, fields=None, raw=False):
    res = base.describe(
        None,
        client().describe_images,
        filters=filters(tags, {}),
        raw=raw,
    )
    if fields:
        return [to_values(i, fields) for i in to_value(res, "Images")]
    return res


@click.group()
@click.pass_context
def ami(ctx):
    pass


@ami.command()
@click.argument("tags", metavar="{key=value}", nargs=-1)
@click.option("--exclude_tag", "-e", default="")
@click.option("--raw", "-r", is_flag=True)
@click.pass_context
def describe(ctx, tags, exclude_tag, raw):
    """List of AMI"""
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

    fields = [] if raw else ["ImageId", "Name", "Tags"]
    res = find(keyvalues(tags), fields=fields, raw=True)
    if raw:
        logs.message(res)
        return

    if exclude_tag:
        key, value = exclude_tag.split("=")
        res = [m for m in res if m["Tags"].get(key, None) != value]

    logs.message(res)
