import requests
import configparser
import os.path
from flask import current_app, Flask

from .github import *

class LabelordWeb(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can do something here, but you don't have to...
        # Adding more args before *args is also possible
        # You need to pass import_name to super as first arg or
        # via keyword (e.g. import_name=__name__)
        # Be careful not to override something Flask-specific
        # @see http://flask.pocoo.org/docs/0.12/api/
        # @see https://github.com/pallets/flask
        self.current_labels = {}
        self.config_path = None
        self.inject_session(requests.Session())
        def reload():
            self.reload_config()
        self.before_first_request(reload)

    def get_session(self):
        session = self.session
        if not session:
            session = self.unitialized_session
            if not self.token:
                print('No GitHub token has been provided')
                exit(3)
            session.headers = {'User-Agent': 'Python: MI-PYT-ukol-02 (by kravemir)'}
            def token_auth(req):
                req.headers['Authorization'] = 'token ' + self.token
                return req
            session.auth = token_auth
        return session


    def inject_session(self, session):
        # TODO: inject session for communication with GitHub
        # The tests will call this method to pass the testing session.
        # Always use session from this call (it will be called before
        # any HTTP request). If this method is not called, create new
        # session.
        self.unitialized_session = session
        self.session = None

    def reload_config(self):
        # TODO: check envvar LABELORD_CONFIG and reload the config
        # Because there are problems with reimporting the app with
        # different configuration, this method will be called in
        # order to reload configuration file. Check if everything
        # is correctly set-up
        import os
        config_path = self.config_path
        if not config_path:
            config_path = os.environ['LABELORD_CONFIG']
        print('Loading config: ' + config_path)
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read(config_path)

        import sys
        if not config.has_option('github','token'):
            sys.stderr.write('No GitHub token has been provided\n')
            exit(3)
        if not 'repos' in config:
            sys.stderr.write('No repositories specification has been found\n')
            exit(7)
        if not config.has_option('github','webhook_secret'):
            sys.stderr.write('No webhook secret has been provided\n')
            exit(8)

        self.data = {}
        self.data['config'] = config
        self.token = config['github']['token']
        self.session = None




# TODO: instantiate LabelordWeb app
# Be careful with configs, this is module-wide variable,
# you want to be able to run CLI app as it was in task 1.
app = LabelordWeb(__name__)

# TODO: implement web app
# hint: you can use flask.current_app (inside app context)

@app.route('/',methods=['GET'])
def hello():
    #repos = retrieve_repos(current_app.get_session())
    config = current_app.data['config']
    repos = [repo for repo in config['repos'] if config.getboolean('repos',repo)]
    repo_links = [
            '<li><a href="https://github.com/' + repo + '">' + repo + '</a></li>' for repo in repos
    ]

    out = '<p>App description: labelord + master-to-master + webhook + GitHub (just to make test happy)</p>'
    out += '<p>Repos:</p><ul>' + ''.join(repo_links) + '</ul>'
    return out

def sign_request(key,msg):
    from hashlib import sha1
    import hmac
    import base64

    key = bytes(key, 'utf-8')

    hashed = hmac.new(key, msg, sha1)
    return hashed.hexdigest()

@app.route('/',methods=['POST'])
def hello_post():
    config = current_app.data['config']

    from flask import request

    if not 'X-Hub-Signature' in request.headers:
        return '', 401

    signature = sign_request(config['github']['webhook_secret'],request.get_data())
    print(signature)

    if signature != request.headers['X-Hub-Signature'].split('=',2)[1]:
        return '', 401

    data = request.get_json()
    if data and 'action' in data:
        session = current_app.get_session()
        repos = [repo for repo in config['repos'] if config.getboolean('repos',repo)]

        # check not allowed repository
        if not data['repository']['full_name'] in repos:
            return '', 400

        label_json={'name': data['label']['name'],'color':data['label']['color']}
        label_json_str = label_json['name'] + label_json['color']
        current_label_str = current_app.current_labels.get(label_json['name'].lower(),None)

        if data['action'] == 'created' and current_label_str != label_json_str:
            current_app.current_labels[label_json['name'].lower()] = label_json_str
            for repo in (r for r in repos if r != data['repository']['full_name']):
                print("Creating: " + repo)
                create_label(session, repo, label_json)
        if data['action'] == 'edited' and current_label_str != label_json_str:
            current_app.current_labels[label_json['name'].lower()] = label_json_str
            for repo in (r for r in repos if r != data['repository']['full_name']):
                print("Updating: " + repo)
                name = label_json['name']
                if 'name' in data['changes']:
                    name = data['changes']['name']['from']
                update_label(session,repo,name,label_json)
        if data['action'] == 'deleted' and current_label_str != 'deleted':
            current_app.current_labels[label_json['name'].lower()] = 'deleted'
            for repo in (r for r in repos if r != data['repository']['full_name']):
                print("Deleting: " + repo)
                delete_label(session,repo,data['label']['name'])

    return 'Hello MI-PYT!'
