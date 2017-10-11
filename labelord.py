# This is skeleton for labelord module
# MI-PYT, task 1 (requests+click)
# File: labelord.py
# TODO: create requirements.txt and install
import click
import requests
import configparser

# Structure your implementation as you want (OOP, FP, ...)
# Try to make it DRY also for your own good


@click.group('labelord')
@click.pass_context
@click.option('--config','config_path')
@click.option('-t','--token',envvar='GITHUB_TOKEN')
def cli(ctx,config_path,token):
    config = configparser.ConfigParser()

    if config_path:
        config.read(config_path)

    if not token and config_path:
        token = config['github']['token']

    # Use this session for communication with GitHub
    session = ctx.obj.get('session', requests.Session())
    session.headers = {'User-Agent': 'Python: MI-PYT-ukol-01 (by kravemir)'}
    def token_auth(req):
        req.headers['Authorization'] = 'token ' + token
        return req
    session.auth = token_auth

    ctx.obj['session'] = session


@cli.command()
@click.pass_context
def list_repos(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'list_repos' command
    session = ctx.obj['session']
    r = session.get('https://api.github.com/user/repos?per_page=100&page=1')
    for repo in r.json():
        print(repo['full_name'])


@cli.command()
@click.pass_context
def list_labels(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'list_labels' command
    ...


@cli.command()
@click.pass_context
def run(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'run' command
    ...


if __name__ == '__main__':
    cli(obj={})
