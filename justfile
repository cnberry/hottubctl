set shell := ["bash", "-cu"]

venv := ".venv"
python := `command -v python3`
pytest := venv + "/bin/pytest"

default:
    just --list

setup:
    {{python}} -m venv {{venv}}
    {{venv}}/bin/pip install -e ".[dev]"

install:
    pipx install --editable .

reinstall:
    -pipx uninstall hottubctl
    pipx install --editable .

test:
    {{venv}}/bin/ruff format --check hottubctl tests
    {{venv}}/bin/ruff check hottubctl tests
    {{venv}}/bin/detect-secrets scan --baseline .secrets.baseline
    PYTHONPATH=. {{pytest}} -q

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
    hottubctl temp set {{value}} --yes
