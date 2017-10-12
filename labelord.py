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
@click.option('-c','--config','config_path')
@click.option('-t','--token',envvar='GITHUB_TOKEN')
def cli(ctx,config_path,token):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option

    if config_path:
        config.read(config_path)

    if not token and config_path:
        token = config['github']['token']

    if not token:
        print('No GitHub token has been provided')
        exit(3)

    # Use this session for communication with GitHub
    session = ctx.obj.get('session', requests.Session())
    session.headers = {'User-Agent': 'Python: MI-PYT-ukol-01 (by kravemir)'}
    def token_auth(req):
        req.headers['Authorization'] = 'token ' + token
        return req
    session.auth = token_auth

    ctx.obj['session'] = session
    ctx.obj['config'] = config


@cli.command()
@click.pass_context
def list_repos(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'list_repos' command

    url = 'https://api.github.com/user/repos?per_page=100&page=1'

    while url:
        session = ctx.obj['session']
        r = session.get(url)
        if r.status_code != 200:
            print("GitHub: ERROR {} - {}".format(r.status_code,r.json()['message']))
            exit(4)
        for repo in r.json():
            print(repo['full_name'])

        if 'next' in r.links:
            url = r.links['next']['url']
        else:
            url = None


@cli.command()
@click.pass_context
@click.argument('slug')
def list_labels(ctx,slug):
    url = 'https://api.github.com/repos/{}/labels?per_page=100&page=1'.format(slug)
    session = ctx.obj['session']
    while url:
        r = session.get(url)
        if r.status_code == 404:
            print("GitHub: ERROR {} - {}".format(r.status_code,r.json()['message']))
            exit(5)
        if r.status_code != 200:
            print("GitHub: ERROR {} - {}".format(r.status_code,r.json()['message']))
            exit(4)
        for label in r.json():
            print('#{} {}'.format(label['color'], label['name']))
        if 'next' in r.links:
            url = r.links['next']['url']
        else:
            url = None


@cli.command()
@click.pass_context
@click.argument('mode')
@click.option('-v','--verbose', default=False, is_flag=True)
@click.option('-q','--quiet', default=False, is_flag=True)
def run(ctx,mode,verbose,quiet):
    config = ctx.obj['config']
    session = ctx.obj['session']
    if not 'labels' in config:
        print('No labels specification has been found')
        exit(6)
    if not 'repos' in config:
        print('No repositories specification has been found')
        exit(7)

    updated_repos = 0
    for repo in config['repos']:
        if not config['repos'][repo] in ['on', 'true']:
            continue

        original_labels = session.get('https://api.github.com/repos/{}/labels?per_page=100&page=1'.format(repo)).json()
        updated_repos = updated_repos + 1
        for label in config['labels']:
            label_json={'name': label,'color':config['labels'][label]}
            match = [l for l in original_labels if label == l['name'] ]
            if len(match) == 0:
                r = session.post('https://api.github.com/repos/{}/labels'.format(repo), json=label_json)
            else:
                if match[0]['color'] != config['labels'][label]:
                    label_url = 'https://api.github.com/repos/{}/labels/{}'.format(repo,label)
                    r = session.patch(label_url,json=label_json)

    print ('SUMMARY: {} repo(s) updated successfully'.format(updated_repos))



if __name__ == '__main__':
    cli(obj={})
