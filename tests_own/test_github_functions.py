
# TODO: should be in labelord.github package
from labelord.cli import retrieve_repos

import configparser
import requests

def test_repos_retrieve():
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

    print (retrieve_repos(session))
