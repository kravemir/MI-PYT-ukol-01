#!/usr/bin/env bash

. __venv__/bin/activate

export FLASK_APP=labelord.py
export LABELORD_CONFIG=config.ini
flask run

