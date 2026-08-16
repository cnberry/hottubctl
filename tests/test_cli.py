from hottubctl.cli import build_parser, cmd_temp_set


def test_temperature_write_requires_yes(capsys):
    assert cmd_temp_set(101, None, False, False) == 2
    assert "without --yes" in capsys.readouterr().err


def test_temperature_parser_accepts_explicit_guard():
    args = build_parser().parse_args(["temp", "set", "101", "--yes"])
    assert args.value == 101
    assert args.yes is True
