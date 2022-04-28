from pathlib import Path

import click
import environ as E

from .aws.commands import aws
from .mysql.commands import mysql
from .base.process import exec_command

# https://django-environ.readthedocs.io/en/latest/


@click.group(help="Tools Subcommand")
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

    ENV = E.Env()
    ENV.read_env(env_file=str(Path.cwd() / ".env"))
    ctx.obj["env"] = ENV


@main.command()
@click.pass_context
def open_terminal(ctx):
    """Open Terminal"""
    exec_command("date", terminal=True)


# sub-subcommands
main.add_command(aws)
main.add_command(mysql)
