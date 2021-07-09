import re
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

import pytest

spec = spec_from_loader("pw", SourceFileLoader("pw", str(Path(__file__).parent.parent.joinpath("pw"))))
pw = module_from_spec(spec)
spec.loader.exec_module(pw)


def test_toml_wraptor_value():
    toml = Path(__file__).with_name("test.toml")
    assert pw.toml_wraptor_value(toml, "tool1") == "tool1 pip"
    assert pw.toml_wraptor_value(toml, "tool2") == "tool2 pip"
    assert pw.toml_wraptor_value(toml, "tool3").split() == ["a", "b", "c"]
    assert pw.toml_wraptor_value(toml, "tool4").split() == ["d", "e"]
    assert pw.toml_wraptor_value(toml, "tool5") == "tool5 pip"
    assert pw.toml_wraptor_value(toml, "tool6") == "tool6 pip"


def test_toml_aliases():
    toml = Path(__file__).with_name("test.toml")
    assert pw.toml_aliases(toml) == {
        "run": "tool1 start",
        "test": "tool2 run test",
        "sub_tool": "tool1 : sub_tool default_arg",
    }


def test_parse_args():
    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "command"])
    assert tool == cmd == "command"
    assert args == []
    assert not upgrade
    assert not clear

    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "command", "arg1", "arg2"])
    assert tool == cmd == "command"
    assert args == ["arg1", "arg2"]
    assert not upgrade
    assert not clear

    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "--upgrade", "command", "arg1"])
    assert tool == cmd == "command"
    assert args == ["arg1"]
    assert upgrade
    assert not clear

    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "--clear", "command"])
    assert tool == cmd == "command"
    assert args == []
    assert not upgrade
    assert clear

    with pytest.raises(Warning, match=f"Python Wraptor version {pw.VERSION}"):
        pw.parse_args(["pw", "--version", "command"])

    with pytest.raises(Warning, match=re.escape(pw.HELP)):
        pw.parse_args(["pw"])


def test_parse_args_with_alias():
    toml = Path(__file__).with_name("test.toml")
    aliases = pw.toml_aliases(toml)

    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "run"], aliases)
    assert tool == cmd == "tool1"
    assert args == ["start"]
    assert not upgrade
    assert not clear

    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "--clear", "test", "my-test"], aliases)
    assert tool == cmd == "tool2"
    assert args == ["run", "test", "my-test"]
    assert not upgrade
    assert clear

    tool, cmd, args, upgrade, clear = pw.parse_args(["pw", "--upgrade", "sub_tool", "arg1", "arg2"], aliases)
    assert tool == "tool1"
    assert cmd == "sub_tool"
    assert args == ["default_arg", "arg1", "arg2"]
    assert upgrade
    assert not clear
