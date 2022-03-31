import click

from .process import exec_command


@click.group()
@click.pass_context
def base(ctx):
    pass


@base.command()
@click.pass_context
def open_terminal(ctx):
    """ Open Terminal"""
    exec_command("date", terminal=True)
