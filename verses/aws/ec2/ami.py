import click

from verses.aws import base
from verses.base import logs

from ..base import args_filters
from .base import client


@click.group()
@click.pass_context
def ami(ctx):
    pass


@ami.command()
@click.argument("tags", metavar="{key=value}", nargs=-1)
@click.option("--raw", "-r", is_flag=True)
@click.pass_context
def describe(ctx, tags, raw):
    """List of AMI"""
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
    res = base.describe(
        None,
        client().describe_images,
        filters=args_filters(*tags),
        raw=True,
    )
    if raw:
        logs.message(res)
        return
    keys = ["ImageId", "Name", "Tags"]
    msg = [dict((i, image.get(i, None)) for i in keys) for image in res["Images"]]
    logs.message(msg)
