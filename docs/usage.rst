Usage guide
===========

Labelord has two components:

* commandline application - easy global label management,
* web-application.

Installation
------------

The application can be installed from test PyPI (not a real application, therefore it's only in test PyPI). And, it's good to install it within virtual environment:

::

    python3.6 -m venv __venv__
    . __venv__/bin/activate
    pip install --extra-index-url https://test.pypi.org/simple/ --user labelord-kravemir

Command line application
------------------------

Command line communicates with GitHub using `REST API v3 <https://developer.github.com/v3/>`_. 

Authentication configuration (REQUIRED)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As actions have to be performed as certain user, authentication is needed. Authentication using name and password can be considered unsafe, therefore application uses personal access tokens.

1. create personal access token for your account: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
2. create :code:`config.ini` file, containing:
    ::

        [github]
        token = YOUR_SECRET_TOKEN

To test it, run :code:`python -m labelord list_repos`, which doesn't modify any data.

Listing commands
^^^^^^^^^^^^^^^^

To retrieve list of your repositories:

::

    python -m labelord list_repos

To retrieve list of labels for repository :code:`username/repo`:

::

    python -m labelord list_labels 'username/repo'

Run command (labels management)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The primary purpose of command-line application is an easy configuration/synchronization of labels.

Run command structure is following:

::

    python -m labelord [GLOBAL_OPTIONS] run <MODE> [RUN_OPTIONS]

Behaviour of run command is configuration driven, and it is configured also in :code:`config.ini`. See `Labels specification`_, and `Repositories specification`_.

Modes:

+----------------------------------+---------------------------------------------------------------+
| Run mode                         | Description                                                   |
+==================================+===============================================================+
| :code:`update`                   | Creates labels, updates colors, keeps extra labels.           |
+----------------------------------+---------------------------------------------------------------+
| :code:`replace`                  | Creates labels, updates colors, deletes extra labels.         |
|                                  |                                                               |
|                                  | WARNING: this performs more destructive changes               |
+----------------------------------+---------------------------------------------------------------+


Labels specification
""""""""""""""""""""

Labels can be specified as list of labels (name = color):

::

    [labels]
    Bug = FF0000
    Last year = 23FB89

Or, a existing repository can be used as a template:

::

    [others]
    template-repo = MarekSuchanek/myLabels

Repositories specification
""""""""""""""""""""""""""

Repositories, on which tool should operate, are specified as list:

::

    [repos]
    MarekSuchanek/repo1 = on
    MarekSuchanek/repo2 = on
    CVUT/MI-PYT = off

Or, tool can operate on all available repositories using option :code:`-a` / :code:`--all-repos`.

Available run options
"""""""""""""""""""""

Run options:

+----------------------------------+---------------------------------------------------------------+
| Run option                       | Description                                                   |
+==================================+===============================================================+
| :code:`-d` / :code:`--dry-run`   | Run in dry mode: no real changes, only print information      |
+----------------------------------+---------------------------------------------------------------+
| :code:`-v` / :code:`--verbose`   | More detailed output                                          |
+----------------------------------+---------------------------------------------------------------+
| :code:`-q` / :code:`--quiet`     | No information to stdout                                      |
+----------------------------------+---------------------------------------------------------------+
| :code:`-a` / :code:`--all-repos` | Performs update on all available repositories (to list_repos) |
+----------------------------------+---------------------------------------------------------------+


Web application
---------------

Would be documented in similar style as Command line application. BUT, since this isn't going to be ever really used by anybody else, I'm not motivated to cover whole documentation. It's a waste of time.

Configuration file: TODO

Run: TODO
