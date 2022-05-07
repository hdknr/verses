import click

from .ec2 import commands


@click.group()
@click.pass_context
def aws(ctx):
    pass


aws.add_command(commands.ec2)
