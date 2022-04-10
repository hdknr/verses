import click


from . import instances


@click.group()
@click.pass_context
def ec2(ctx):
    pass


ec2.add_command(instances.instances)
