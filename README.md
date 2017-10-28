# MI-PYT-ukol-01

Run tests:

```bash
python3.5 -m venv __venv__
. __venv__/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest labelord.py tests_cli/ 2>/dev/null
python -m pytest labelord.py tests_web/ 2>/dev/null
```

Run new tests:

```bash
python3.6 -m venv __venv__
. __venv__/bin/activate
pip install -r requirements.txt 

export CTU_USERNAME=kravemir
export LABELORD_REPO='git@github.com:kravemir/MI-PYT-ukol-01.git'
export LABELORD_BRANCH=modules

python -m pytest tests_module/test_submodules.py 
```

Tested on:

```bash
$ python --version
Python 3.5.3
$ pip --version
pip 9.0.1 from /home/...
$ pip freeze
betamax==0.8.0
certifi==2017.7.27.1
chardet==3.0.4
click==6.7
configparser==3.5.0
flexmock==0.10.2
idna==2.6
pkg-resources==0.0.0
py==1.4.34
pytest==3.2.3
requests==2.18.4
urllib3==1.22
```
