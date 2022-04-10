import click

from . import ami, instances


@click.group()
@click.pass_context
def ec2(ctx):
    pass


ec2.add_command(instances.instances)
ec2.add_command(ami.ami)
