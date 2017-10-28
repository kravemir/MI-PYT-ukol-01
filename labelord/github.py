
def create_label(session, repo, json):
    return session.post('https://api.github.com/repos/{}/labels'.format(repo), json = json)

def update_label(session, repo, original_name, json):
    return session.patch(
            'https://api.github.com/repos/{}/labels/{}'.format(repo,original_name),
            json = json
    )

def delete_label(session, repo, name):
    return session.delete('https://api.github.com/repos/{}/labels/{}'.format(repo,name))
