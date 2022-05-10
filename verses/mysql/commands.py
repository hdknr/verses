import click
from string import Template
import sys


@click.group()
@click.pass_context
def mysql(ctx):
    pass

def open_stream(path=None):
    return  path and open(path, "w") or sys.stdout

def write_template(templ, path=None, **params):
    sql = templ.substitute(**params)
    with open_stream(path) as out:
        out.write(sql)


@mysql.command(help="Create Database Script")
@click.option("--path", "-p", default=None)
@click.option("--database_url", "-d", default="DATABASE_URL")
@click.pass_context
def create_database_script(ctx, path, database_url):
    """ Create Database Script """
    db = ctx.obj["env"].db_url(database_url)
    templ = Template(
        """
CREATE DATABASE IF NOT EXISTS $NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER IF NOT EXISTS '$USER'@'%' IDENTIFIED BY '$PASSWORD';
GRANT ALL PRIVILEGES ON $NAME.*  TO '$USER'@'%';
flush privileges;
SHOW GRANTS FOR '$USER'@'%';
    """
    )
    write_template(templ, path=path, **db)


@mysql.command(help="mysqldump")
@click.option("--path", "-p", default=None)
@click.option("--database_url", "-d", default="DATABASE_URL")
@click.option("--mode", "-m", default="all")
@click.pass_context
def dump(ctx, path, database_url, mode):
    """ MySQL Dump """
    db = ctx.obj["env"].db_url(database_url)

    opt = {"all": "", "data": "--no-create-info",  "ddl": "--no-data"}[mode]
    opt = f"{opt} --skip-extended-insert --set-gtid-purged=OFF  --complete-insert"
    templ = Template(
        "mysqldump -h $HOST -u $USER $OPT -p$PASSWORD $NAME"
    )
    write_template(templ, OPT=opt, **db)



@mysql.command(help="MySQL ROOT user client")
@click.option("--path", "-p", default=None)
@click.option("--database_url", "-d", default="DATABASE_URL")
@click.pass_context
def shell(ctx, database_url):
    """ MySQL Root Client """
    db = ctx.obj["env"].db_url(database_url)
    templ = Template("mysql -h $HOST -u $USER -p$PASSWORD $NAME")
    write_template(templ, **db)