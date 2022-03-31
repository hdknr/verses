import click

from . import instance
from verses.base import remote


@click.group()
@click.pass_context
def ec2(ctx):
    pass


@ec2.command()
@click.argument("user")
@click.argument("tags", nargs=-1)
@click.pass_context
def ssh(ctx, user, tags):
    """ ssh to EC2 instance"""
    filters = [
        {"Name": f"tag:{k}", "Values": [v]} for k, v in [i.split("=") for i in tags]
    ]
    res = instance.query(None, filters=filters)

    if len(res.Reservations) == 1:
        keyname = res.Reservations[0].Instances[0].KeyName
        key = remote.ssh_keyfile(f"{keyname}.cer", f"{keyname}.pem")
        if not key:
            print(f"{keyname} was not found.")
            return
        remote.exec_ssh(user, res.Reservations[0].Instances[0].PublicIpAddress, str(key))
        return
    
    # TODO:
    # list of instances
