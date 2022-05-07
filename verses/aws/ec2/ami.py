import click

from verses.base import logs

from ..base import keyvalues
from .base_ami import find


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
