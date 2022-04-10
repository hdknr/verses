from datetime import datetime

import click

from verses.aws.base import Object, call
from verses.base import logs, remote

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


@click.group()
@click.pass_context
def instances(ctx):
    pass


@instances.command()
@click.argument("name")
@click.option("--user", "-u", default="ubuntu")
@click.pass_context
def ssh_conf(ctx, name, user):
    """create ssh config file to EC2 instance"""
    instance = query_by_name(None, name)
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    if not instance:
        logs.message(dict(error=f"no instance of {name}"))
        return

    keyname, ipaddress = instance.KeyName, instance.PublicIpAddress

    key = remote.ssh_keyfile(f"{keyname}.cer", f"{keyname}.pem")
    if not key:
        logs.message(dict(error=f"{keyname} was not found."))
        return

    remote.update_ssh_conf(
        name,
        user,
        "server",
        ipaddress,
        str(key),
    )


@instances.command()
@click.argument("name")
@click.argument("tags", metavar="{key=value}", nargs=-1)
@click.option("--suffix", "-s", default=None)
@click.option("--reboot", "-r", is_flag=True)
@click.option("--dry_run", "-d", is_flag=True)
@click.pass_context
def create_image(ctx, name, tags, suffix, reboot, dry_run):
    """create ami for named instance

    sample:
    create-image
        prod-masters myservice-deploy=prod myservice-server=masters
            serial=$(date +"%Y%m%d%H%M%S") --suffix $(date +"%Y%m%d%H%M%S")
    """
    instance = query_by_name(None, name)
    if not instance:
        logs.message(dict(error=f"no instance of {name}"))
        return

    now = datetime.now()
    suffix = suffix or now.strftime("%Y%m%d")

    instance_id = instance.InstanceId
    name = f"{name}-{suffix}"
    keyvalues = dict(tuple(t.split("=")) for t in tags)
    tag_specs = instances.tag_specifications("image", keyvalues)

    res = call(
        client().create_image,
        InstanceId=instance_id,
        Name=name,
        TagSpecifications=tag_specs,
        NoReboot=not reboot,
        DryRun=dry_run,
    )
    logs.message(res)
