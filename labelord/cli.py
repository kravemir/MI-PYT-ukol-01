import click
import os
import requests
import configparser
import os.path

from .github import *

@click.group('labelord',invoke_without_command=True)
@click.pass_context
@click.option('--version',is_flag=True)
@click.option('-c','--config','config_path',type=click.Path(exists=True))
@click.option('-t','--token',envvar='GITHUB_TOKEN')
def cli(ctx,config_path,token,version):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option

    if config_path and os.path.isfile(config_path):
        config.read(config_path)
    elif os.path.isfile('config.ini'):
        config.read('config.ini')

    if not token and config.has_option('github','token'):
        token = config['github']['token']

    # Use this session for communication with GitHub
    original_session = ctx.obj.get('session', requests.Session())
    session_storage = []
    def make_session():
        if len(session_storage) == 0:
            if not token:
                print('No GitHub token has been provided')
                exit(3)
            session = original_session
            session.headers = {'User-Agent': 'Python: MI-PYT-ukol-01 (by kravemir)'}
            def token_auth(req):
                req.headers['Authorization'] = 'token ' + token
                return req
            session.auth = token_auth
            session_storage.append(session)
        return session_storage[0]

    ctx.obj['session'] = make_session
    ctx.obj['config'] = config
    ctx.obj['config_path'] = config_path

    if version:
        print('labelord, version 0.1')

def retrieve_repos(session):
    repos = []
    url = 'https://api.github.com/user/repos?per_page=100&page=1'

    while url:
        r = session.get(url)
        if r.status_code != 200:
            print("GitHub: ERROR {} - {}".format(r.status_code,r.json()['message']))
            exit(4)
        for repo in r.json():
            repos.append(repo)

        if 'next' in r.links:
            url = r.links['next']['url']
        else:
            url = None
    return repos

@cli.command()
@click.pass_context
def list_repos(ctx):
    session = ctx.obj['session']()
    for repo in retrieve_repos(session):
        print(repo['full_name'])

def retrieve_labels(ctx,slug):
    labels = []
    url = 'https://api.github.com/repos/{}/labels?per_page=100&page=1'.format(slug)
    session = ctx.obj['session']()
    while url:
        r = session.get(url)
        if r.status_code == 404:
            print("GitHub: ERROR {} - {}".format(r.status_code,r.json()['message']))
            exit(5)
        if r.status_code != 200:
            print("GitHub: ERROR {} - {}".format(r.status_code,r.json()['message']))
            exit(4)
        for label in r.json():
            labels.append(label)
        if 'next' in r.links:
            url = r.links['next']['url']
        else:
            url = None
    return labels

@cli.command()
@click.pass_context
@click.argument('slug')
def list_labels(ctx,slug):
    for label in retrieve_labels(ctx,slug):
        print('#{} {}'.format(label['color'], label['name']))

@cli.command()
@click.pass_context
@click.argument('mode',type=click.Choice(['update','replace']))
@click.option('-v','--verbose', default=False, is_flag=True)
@click.option('-q','--quiet', default=False, is_flag=True)
@click.option('-a','--all-repos', 'all_repos', default=False, is_flag=True)
@click.option('-d','--dry-run', 'dry_run', default=False, is_flag=True)
@click.option('-r','--template-repo', 'template_repo' )
def run(ctx,mode,verbose,quiet,all_repos,dry_run, template_repo):
    config = ctx.obj['config']
    session = ctx.obj['session']()

    # fallback to config
    if not template_repo and 'others' in config and 'template-repo' in config['others']:
        template_repo = config['others']['template-repo']

    # get list of labels to update, if not defined, print error and exit(6)
    labels = None
    if template_repo:
        labels = [(label['name'],label['color']) for label in retrieve_labels(ctx,template_repo)]
    elif 'labels' in config:
        labels = [(label,config['labels'][label]) for label in config['labels']]
    else:
        print('No labels specification has been found')
        exit(6)

    # get list of repositories to update, if not defined, print error and exit(7)
    repos = None
    if all_repos:
        repos = [repo['full_name'] for repo in retrieve_repos(session)]
    elif 'repos' in config:
        repos = [repo for repo in config['repos'] if config.getboolean('repos',repo)]
    else:
        print('No repositories specification has been found')
        exit(7)

    updated_repos = 0
    update_errors = [0]

    def log_error(tag,text,response):
        update_errors[0] += 1
        if not quiet:
            text = text + "; {} - {}".format(response.status_code,response.json()['message'])
            if verbose:
                print("[{}][ERR] {}".format(tag,text))
            else:
                print("ERROR: {}; {}".format(tag,text))

    # just to utilize github.py
    def run_function(tag, text, text_params, fn, args, expected_status):
        if dry_run:
            # in dry run print operation to output, but only in non-quiet verbose mode
            if not quiet and verbose:
                print("[{}][DRY] {}".format(tag,text.format(*text_params)))
        else:
            # perform command, and print log to output
            r = fn(session, *args)
            if r.status_code != expected_status:
                log_error(tag,text.format(*text_params),r)
            elif verbose and not quiet:
                print('[{}][SUC] '.format(tag) + text.format(*text_params))

    for repo in repos:
        original_labels_r = session.get('https://api.github.com/repos/{}/labels?per_page=100&page=1'.format(repo))
        if original_labels_r.status_code != 200:
            log_error('LBL',repo,original_labels_r)
            continue
        original_labels = original_labels_r.json()
        updated_repos = updated_repos + 1
        for label,color in labels:
            label_json={'name': label,'color':color}
            match = [l for l in original_labels if label.lower() == l['name'].lower() ]
            if len(match) == 0:
                run_function(
                    'ADD', '{}; {}; {}', [repo,label,color],
                    create_label, [repo, label_json], 201
                )
            else:
                if match[0]['color'] != color or match[0]['name'] != label:
                    run_function(
                        'UPD', '{}; {}; {}', [repo,label,color],
                        update_label, [repo, match[0]['name'], label_json], 200
                    )
        if mode == 'replace':
            label_names = [ name for name,color in labels ]
            for label in (label for label in original_labels if not label['name'] in label_names):
                run_function(
                    'DEL', '{}; {}; {}', [repo,label['name'],label['color']],
                    delete_label, [repo,label['name']], 204
                )


    if update_errors[0] == 0:
        if verbose and not quiet:
            print ('[SUMMARY] {} repo(s) updated successfully'.format(updated_repos))
        elif (verbose and quiet) or not quiet:
            print ('SUMMARY: {} repo(s) updated successfully'.format(updated_repos))
    else:
        if verbose and not quiet:
            print ('[SUMMARY] {} error(s) in total, please check log above'.format(update_errors[0]))
        elif (verbose and quiet) or not quiet:
            print ('SUMMARY: {} error(s) in total, please check log above'.format(update_errors[0]))
        exit(10)

if __name__ == '__main__':
    cli(obj={})
