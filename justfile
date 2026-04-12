set shell := ["bash", "-cu"]

venv := ".venv"
python := `command -v python3`
pytest := venv + "/bin/pytest"

default:
    just --list

setup:
    {{python}} -m venv {{venv}}
    {{venv}}/bin/pip install -e .
    {{venv}}/bin/pip install pytest

install:
    pipx install --editable .

reinstall:
    -pipx uninstall hottubctl
    pipx install --editable .

test:
    {{python}} -m py_compile hottubctl.py hottubctl/*.py
    if [ -x {{pytest}} ]; then PYTHONPATH=. {{pytest}} -q; else echo 'pytest not installed; run just setup'; fi

test-integration:
    hottubctl spas >/dev/null

test-all:
    just test
    just test-integration

spas:
    hottubctl spas

status:
    hottubctl temp get

temp-get:
    hottubctl temp get

temp-set value:
    hottubctl temp set {{value}}
