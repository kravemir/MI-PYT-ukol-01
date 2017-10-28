import click

from .cli import cli
from .web import app

@cli.command()
@click.option('-h','--host')
@click.option('-p','--port')
@click.option('-d','--debug', default=False, is_flag=True)
@click.pass_context
def run_server(ctx,host,port,debug):
    # TODO: implement the command for starting web app (use app.run)
    # Don't forget to app the session from context to app
    app.config_path = ctx.obj['config_path']
    app.reload_config()
    app.run(host,port,debug)

def main():
    cli(obj={})
