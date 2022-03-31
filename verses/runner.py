from pathlib import Path

import click
import environ as E

from .aws import commands

# https://django-environ.readthedocs.io/en/latest/


@click.group(help="Tools Subcommand")
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

    ENV = E.Env()
    ENV.read_env(env_file=str(Path.cwd() / ".env"))
    ctx.obj["env"] = ENV


main.add_command(commands.aws)
