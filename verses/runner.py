import json
from string import Template

import click
import environ as E
from app import settings
from . import remote

# https://django-environ.readthedocs.io/en/latest/


@click.group(help="Tools Subcommand")
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

    ENV = E.Env()
    ENV.read_env(env_file=str(E.Path(__file__) - 2))
    ctx.obj["env"] = ENV


@main.command(help="Init Django Migrations")
@click.option("--rebuild-files", "-r", is_flag=True)
@click.pass_context
def reset_migration_script(ctx, rebuild_files):
    """ Initialize Django Migrations """
    print("""echo "delete from django_migrations" | python web/manage.py dbshell""")

    if rebuild_files:
        for i in settings.PROJECT_APPS:
            print(f"rm -r web/{i}/migrations/0*.py")
        print("python web/manage.py makemigrations")

    print("python web/manage.py migrate --fake")


@main.command(help="Create Database Script")
@click.pass_context
def create_database_script(ctx):
    """ Create Database Script """
    db = ctx.obj["env"].db_url("DATABASE_URL")
    templ = Template(
        """
CREATE DATABASE IF NOT EXISTS $NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER IF NOT EXISTS '$USER'@'%' IDENTIFIED BY '$PASSWORD';
GRANT ALL PRIVILEGES ON $NAME.*  TO '$USER'@'%';
flush privileges;
SHOW GRANTS FOR '$USER'@'%';
    """
    )
    sql = templ.substitute(**db)
    print(sql)


@main.command(help="mysqldump")
@click.option("--database_url", "-d", default="DATABASE_URL")
@click.pass_context
def mysqldump(ctx, database_url):
    """ MySQL Dump """
    db = ctx.obj["env"].db_url(database_url)
    command = Template(
        "mysqldump -h $HOST -u $USER --set-gtid-purged=OFF -p$PASSWORD $NAME"
    ).substitute(**db)
    print(command)


@main.command(help="MySQL ROOT user client")
@click.option("--name", "-n")
@click.pass_context
def mysql(ctx, name="RDS_MASTER_URL"):
    """ MySQL Root Client """
    db = ctx.obj["env"].db_url(name)
    templ = Template("mysql -h $HOST -u $USER -p$PASSWORD")
    sql = templ.substitute(**db)
    print(sql)


@main.command(
    help="ssh", context_settings=dict(ignore_unknown_options=True,),
)
@click.argument("params", nargs=-1, type=click.UNPROCESSED)
@click.option("--terminal", "-t", is_flag=True)
@click.pass_context
def ssh(ctx, params, terminal):
    """ ssh """
    return remote.ssh(ctx, params, terminal)


@main.command(
    help="scp", context_settings=dict(ignore_unknown_options=True,),
)
@click.argument("params", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def scp(ctx, params):
    """ scp """
    return remote.scp(ctx, params)


@main.command(
    help="rsync", context_settings=dict(ignore_unknown_options=True,),
)
@click.argument("params", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def rsync(ctx, params):
    """ rysnc """
    return remote.rsync(ctx, params)


@main.command(help="download")
@click.argument("remote_dir")
@click.argument("local_dir")
@click.pass_context
def download(ctx, remote_dir, local_dir):
    """ download: ssh tar"""
    return remote.download(ctx, remote_dir, local_dir)


@main.command(help="Dump Environment")
@click.pass_context
def env_dump(ctx):
    """ Dump Environment  in JSON """
    # list all : env-dump | jq ".|to_entries|map(.key)"
    e = ctx.obj["env"]
    data = dict((key, value) for key, value in e.ENVIRON.items())
    print(json.dumps(data))
