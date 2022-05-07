from datetime import datetime

import click

from verses.aws.base import call, keyvalues, tag_specs
from verses.base import logs, remote

from . import base_ami
from .base import client
from .base_instances import query_by_name


@click.group()
@click.pass_context
def instances(ctx):
    pass


@instances.command()
@click.argument("name")
@click.pass_context
def describe(ctx, name):
    """describe"""
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    instance = query_by_name(None, name, raw=True)
    logs.message(instance)


@instances.command()
@click.argument("name")
@click.option("--user", "-u", default="ubuntu")
@click.option("--secrets_dir", "-s", default=None)
@click.pass_context
def ssh_conf(ctx, name, user, secrets_dir):
    """create ssh config file to EC2 instance"""
    instance = query_by_name(None, name)
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    if not instance:
        logs.message(dict(error=f"no instance of {name}"))
        return

    keyname, ipaddress = instance.KeyName, instance.PublicIpAddress

    key = remote.ssh_keyfile(f"{keyname}.cer", f"{keyname}.pem", secrets_dir=secrets_dir)
    if not key:
        logs.message(dict(error=f"{keyname} was not found."))
        return

    remote.update_ssh_conf(
        name,
        user,
        "server",
        ipaddress,
        str(key),
        secrets_dir=secrets_dir,
    )


@instances.command()
@click.argument("name")
@click.argument("tags", metavar="{key=value}", nargs=-1)
@click.option("--latest", "-l", is_flag=True)
@click.option("--suffix", "-s", default=None)
@click.option("--reboot", "-r", is_flag=True)
@click.option("--dry_run", "-d", is_flag=True)
@click.pass_context
def create_image(ctx, name, tags, latest, suffix, reboot, dry_run):
    """create ami for named instance

    sample:
    create-image
        prod-masters myservice-deploy=prod myservice-server=masters
            serial=$(date +"%Y%m%d%H%M%S") --suffix $(date +"%Y%m%d%H%M%S")
    """
    LATEST = {"latest": "true"}
    now = datetime.now()
    suffix = suffix or now.strftime("%Y%m%d")

    # Find Instance
    instance = query_by_name(None, name)
    if not instance:
        logs.message(dict(error=f"no instance of {name}"))
        return

    # AMI Searching
    searching = keyvalues(tags, extra=LATEST if latest else {})

    # Intance Tags
    tags = tag_specs({"Name": name, **searching}, resource_type="image")

    res = call(
        client().create_image,
        InstanceId=instance.InstanceId,
        Name=f"{name}-{suffix}",
        TagSpecifications=tags,
        NoReboot=not reboot,
        DryRun=dry_run,
    )

    if latest and not dry_run:
        imaged_id = res["ImageId"]
        base_ami.remove_tags(searching, exclude_ids=[imaged_id], removing=LATEST)

    logs.message(res)
