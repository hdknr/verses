import click

from . import instance


@click.group()
@click.pass_context
def ec2(ctx):
    pass


@ec2.command()
@click.argument("tags", nargs=-1)
@click.pass_context
def ssh(ctx, tags):
    print(ctx.obj["env"])
    filters = [
        {"Name": f"tag:{k}", "Values": [v]} for k, v in [i.split("=") for i in tags]
    ]
    res = instance.query(None, filters=filters)
    if len(res.Reservations):
        print(res.Reservations[0].Instances[0].PublicIpAddress)
        print(res.Reservations[0].Instances[0].KeyName)
        return
    breakpoint()
