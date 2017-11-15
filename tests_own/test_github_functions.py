
# TODO: should be in labelord.github package
from labelord.cli import retrieve_repos
from labelord.github import *

import configparser
import requests
import pytest

@pytest.fixture
def session():
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

def test_repos_retrieve(session):
    # TODO: check result
    result = retrieve_repos(session)
    assert 0 == 1

@pytest.mark.parametrize(
    ['repo', 'name', 'color', 'result_code' ],
    [
        ('kravemir/config', 'improvement', 'AACC99', 201),
        ('kravemir/config', 'bug', 'AACC99', 422),
        ('kravemir/not-existing-repo', 'new_label', '123456', 404),
    ]
)
def test_create_label(session, repo, name, color, result_code):
    # TODO: check result
    result = create_label(session, repo, {'name': name, 'color': color})

    assert result.status_code == result_code

def test_update_label(session):
    # TODO: check result
    result = update_label(session, 'kravemir/config', 'bug', {'name': 'bug', 'color': '771100'})

    assert result.status_code == 200

def test_delete_label(session):
    # TODO: check result
    result = delete_label(session, 'kravemir/config', 'bug')

    assert result.status_code == 204
