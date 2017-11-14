
# TODO: should be in labelord.github package
from labelord.cli import retrieve_repos
from labelord.github import *

import configparser
import requests

def make_session():
    # TODO: ???
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read('config.ini')
    token = config['github']['token']
    original_session = requests.Session()
    session = original_session
    session.headers = {'User-Agent': 'Python: MI-PYT-ukol-01 (by kravemir)'}
    def token_auth(req):
        req.headers['Authorization'] = 'token ' + token
        return req
    session.auth = token_auth
    return session

def test_repos_retrieve():
    # TODO: ???
    session = make_session()

    # TODO: check result
    result = retrieve_repos(session)
    assert 0 == 1

def test_create_label():
    # TODO: ???
    session = make_session()

    # TODO: check result
    result = create_label(session, 'kravemir/config', {'name': 'improvement', 'color': 'AACC99'})

    assert result.status_code == 201

def test_delete_label():
    # TODO: ???
    session = make_session()

    # TODO: check result
    result = delete_label(session, 'kravemir/config', 'bug')

    assert result.status_code == 204
