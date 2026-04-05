set shell := ["bash", "-cu"]

python := `command -v python3`

default:
    just --list

install:
    pipx install --editable .

reinstall:
    -pipx uninstall hottubctl
    pipx install --editable .

test:
    {{python}} -m py_compile hottubctl.py hottubctl/*.py

spas:
    hottubctl spas

status:
    hottubctl temp get

temp-get:
    hottubctl temp get

temp-set value:
    hottubctl temp set {{value}}
