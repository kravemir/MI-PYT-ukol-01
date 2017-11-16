# MI-PYT-ukol-01

Run:

```bash
# clone and enter directory
git clone git@github.com:kravemir/MI-PYT-ukol-01.git
cd MI-PYT-ukol-01/
git checkout v0.3

# install venv and required packages
python3.6 -m venv __venv__
. __venv__/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt 

# run code tests
python -m pytest tests_cli/
python -m pytest tests_web/

# export properties for module tests
export CTU_USERNAME=kravemir
export LABELORD_REPO='git@github.com:kravemir/MI-PYT-ukol-01.git'
export LABELORD_BRANCH=v0.3

# run module tests
python -m pytest tests_module/

deactivate
```

Run own tests:

```bash
# run tests without recording, using recorded cassettes
python -m pytest tests_own/test_github_functions.py --verbose
```

Record cassettes:

```bash
# delete old cassettes
rm tests_own/fixtures/cassettes/*.json

# read and export token variable
cat config.ini
read GITHUB_TOKEN
export GITHUB_TOKEN

# MANUAL
# CLEANUP REPOSITORIES, check test parameters to match status!!!
# properly configure: config.ini
# run: python -m labelord run replace
# MANUAL

# run tests with recording
python -m pytest tests_own/test_github_functions.py --verbose

# unset env variable
unset GITHUB_TOKEN
```
