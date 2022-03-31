import click

from verses.aws.base import filters
from verses.base import remote

from . import instance


@click.group()
@click.pass_context
def ec2(ctx):
    pass


@ec2.command()
@click.argument("name")
@click.option("--user", "-u", default="ubuntu")
@click.pass_context
def ssh_conf(ctx, name, user):
    """ ssh to EC2 instance """
    res = instance.query(None, filters=filters(("Name", name)))

    if len(res.Reservations) == 1:
        keyname = res.Reservations[0].Instances[0].KeyName
        key = remote.ssh_keyfile(f"{keyname}.cer", f"{keyname}.pem")
        if not key:
            print(f"{keyname} was not found.")
            return

        remote.update_ssh_conf(
            name,
            user,
            "server",
            res.Reservations[0].Instances[0].PublicIpAddress,
            str(key),
        )
