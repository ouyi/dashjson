[![Build Status](https://travis-ci.org/ouyi/dashjson.svg?branch=master)](https://travis-ci.org/ouyi/dashjson)

# dashjson.py -- a Datadog tool

A tool for exporting (or importing) Datadog dashboards to (or from) json. It allows the Datadog dashboard definitions to be

- version controlled as json files, and
- migrated across Datadog accounts

Tested with Python 3.6.7 and datadog 0.26.0.

## How to use

Create the credentials file containing the api\_key and the app\_key. Example content of the credentials file (your keys can be found at https://app.datadoghq.com/account/settings#api):

    # cat ~/.dashjson.json
    {
        "api_key": "abcdefg12345678",
        "app_key": "abcdefg987654321"
    }

Show usage of the tool:

    python dashjson.py -h

## How to build (for contributors only)

These are the steps I used on Ubuntu 18.04.

Add the following lines to `~/.bashrc`:

    # Due to https://github.com/pypa/pipenv/issues/2122
    export PATH="${HOME}/.local/bin:$PATH"

    # Due to https://github.com/pypa/pipenv/issues/1382
    export PIPENV_VENV_IN_PROJECT=true

Install pip and pipenv:

    sudo apt install python3-pip
    python3 -m pip install --user pipenv

Clone and install locally:

    git clone git@github.com:ouyi/dashjson.git
    cd dashjson
    pipenv install --dev
    pipenv run python -m unittest
    pipenv run python dashjson.py -h

## TODOs

1. Automatically determine the dashboard type

For import, the information is available in the input file. For export, we can first [get a list of all screenboards](https://docs.datadoghq.com/api/?lang=python#get-all-screenboards) and then check existence by id.

2. Embed a code coverage badge

The coverage data can be generated with:

    coverage run --source=dashjson -m unittest && coverage report && coverage-badge -f -o coverage.svg
