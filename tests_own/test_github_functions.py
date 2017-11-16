
# TODO: should be in labelord.github package
from labelord.cli import retrieve_repos
from labelord.github import *

import configparser
import requests
import pytest
import betamax
import os

with betamax.Betamax.configure() as config:
    if 'GITHUB_TOKEN' in os.environ:
        # If the tests are invoked with an AUTH_FILE environ variable
        TOKEN = os.environ['GITHUB_TOKEN']
        # Always re-record the cassetes
        # https://betamax.readthedocs.io/en/latest/record_modes.html
        config.default_cassette_options['record_mode'] = 'all'
    else:
        TOKEN = 'false_token'
        # Do not attempt to record sessions with bad fake token
        config.default_cassette_options['record_mode'] = 'none'

    # Hide the token in the cassettes
    config.define_cassette_placeholder('<TOKEN>', TOKEN)
    config.cassette_library_dir = 'tests_own/fixtures/cassettes'

@pytest.fixture
def session(betamax_parametrized_session):
    if 'GITHUB_TOKEN' in os.environ:
        TOKEN = os.environ['GITHUB_TOKEN']
    else:
        TOKEN = 'false_token'

    original_session = betamax_parametrized_session or requests.Session()
    session = original_session
    session.headers = {'User-Agent': 'Python: MI-PYT-ukol-01 (by kravemir)'}
    def token_auth(req):
        req.headers['Authorization'] = 'token ' + TOKEN
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
