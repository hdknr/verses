import click

from verses.base import logs

from ..base import keyvalues
from . import ami, instances
from .base import delete_tags as base_delete_tags


@click.group()
@click.pass_context
def ec2(ctx):
    pass


ec2.add_command(instances.instances)
ec2.add_command(ami.ami)


@ec2.command()
@click.argument("res_or_tags", nargs=-1)
@click.option("--dry_run", "-d", is_flag=True)
@click.pass_context
def delete_tags(ctx, res_or_tags, dry_run=False):
    """
    ami-xxxxx ami-yyyyy latest=true
    """
    resources = [i for i in res_or_tags if i.find("=") < 0]
    if not resources:
        logs.message("no resource specified.")
        return

    tags = keyvalues(res_or_tags)
    return base_delete_tags(resources, tags, dry_run=dry_run)
