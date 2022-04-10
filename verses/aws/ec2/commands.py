import click

from ..base import call, keyvalue_list
from . import ami, instances
from .base import client


@click.group()
@click.pass_context
def ec2(ctx):
    pass


ec2.add_command(instances.instances)
ec2.add_command(ami.ami)


@ec2.command()
@click.argument("res_or_args", nargs=-1)
@click.option("--dry_run", "-d", is_flag=True)
@click.pass_context
def delete_tags(ctx, res_or_args, tags=None, dry_run=False):
    """
    ami-xxxxx ami-yyyyy latest=true
    """
    resources = [i for i in res_or_args if i.find("=") < 0]
    tags = keyvalue_list(res_or_args)
    kwargs = dict(
        Resources=resources,
        DryRun=dry_run,
    )
    if tags:
        kwargs["Tags"] = tags

    return call(client().delete_tags, **kwargs)
