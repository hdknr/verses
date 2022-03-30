import click


@click.group()
@click.pass_context
def ec2(ctx):
    pass


@ec2.command()
@click.pass_context
def ssh(ctx):
    print(ctx.obj["env"])
    click.echo('your running aws ec2 ssh command')