# MI-PYT-ukol-01

Run:

```bash
# clone and enter directory
git clone git@github.com:kravemir/MI-PYT-ukol-01.git
cd MI-PYT-ukol-01/
git checkout modules

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
export LABELORD_BRANCH=modules

# run module tests
python -m pytest tests_module/

deactivate
```
