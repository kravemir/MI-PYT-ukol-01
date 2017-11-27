Usage guide
===========

Labelord has two components:

* commandline application - easy global label management,
* web-application.

Installation
------------

TODO

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

Bla bla bla:

::

    python -m labelord [GLOBAL_OPTIONS] run <MODE> [RUN_OPTIONS]

Modes:

+----------------------------------+---------------------------------------------------------------+
| Run mode                         | Description                                                   |
+==================================+===============================================================+
| :code:`update`                   | Creates labels, updates colors, keeps extra labels.           |
+----------------------------------+---------------------------------------------------------------+
| :code:`replace`                  | Creates labels, updates colors, deletes extra labels.         |
+----------------------------------+---------------------------------------------------------------+

Behaviour is configured in :code:`config.ini`:


Example run configurations
""""""""""""""""""""""""""

TODO

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

TODO
